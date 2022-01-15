import math
import random

from flask import request
from flask_restful import Resource
from flask_bcrypt import generate_password_hash

from app.common.config import Config
from app.common.utilities import Utils
from app.common.email import Email
from app.common.rds import RDS
from schema import Schema, And, Use
from http import HTTPStatus
import bleach


class SignupApi(Resource):
    def __init__(self):
        self.rds = RDS()
        self.schema = Schema({
            'email': And(str, Use(bleach.clean), Utils.validate_email),
            'password': And(str, Use(bleach.clean), Utils.validate_password)
        }, ignore_extra_keys=True)

    def post(self):
        if not self.schema.is_valid(request.get_json()):
            return {'error': 'Invalid Input'}, HTTPStatus.BAD_REQUEST

        data = self.schema.validate(request.get_json())
        email = data['email']
        password = self.hash_password(data['password'])

        user = self.rds.get_user(email=email)

        if user and user['verified']:
            return {"error": "There already exists an account with this email address"}, HTTPStatus.BAD_REQUEST

        user_id = self.rds.create_user(email=email,
                                       password=password)
        self.initiate_verification(user_id=user_id, email=email)

    def hash_password(self, password):
        return generate_password_hash(password).decode('utf8')

    def initiate_verification(self, *, user_id, email):
        otp = self.get_otp()
        self.rds.save_otp(user_id=user_id, otp=otp)

        # TODO: think of a better way to identify the user for verication instead of sending email in url
        msg = f"OTP={otp} \n Link={Config.DOMAIN_NAME}/auth/verify/{email}"
        subject = f"user verification for {Config.COMPANY_NAME} url-shortener service"
        to = [email]
        self.send_email(msg=msg, to=to, subject=subject)

    def send_email(self, *, msg, to, subject):
        email = Email()
        email.login()
        body = email.create_msg(message_text=msg, to=to, subject=subject)
        email.send_msg(message=body)

    def get_otp(self):
        digits = Config.OTP_DIGIT_SPACE
        OTP = ""
        for i in range(6):
            OTP += digits[math.floor(random.random() * 10)]
        return OTP
