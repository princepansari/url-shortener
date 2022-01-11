import math
import random

from flask import request
from flask_restful import Resource
from flask_bcrypt import generate_password_hash
from app.auth.src.common.utilities import Utils
from app.auth.src.common.email import Email
from app.auth.src.common.rds import RDS


class SignupApi(Resource):
    def __init__(self):
        self.rds = RDS()

    def post(self):
        data = Utils.sanitize_dict(request.get_json())
        email = data['email']
        password = self.hash_password(data['password'])
        user_id = self.rds.create_user(email=email,
                             password=password)
        self.initiate_verification(user_id=user_id, email=email)

    def hash_password(self, password):
        return generate_password_hash(password).decode('utf8')

    def initiate_verification(self, *, user_id, email):
        otp = self.get_otp()
        self.rds.save_otp(user_id=user_id, otp=otp)
        # TODO: think of a better way to identify the user for verication instead of sending email in url
        msg = f"OTP={otp} \n Link=https://three-unicorns.com/auth/verify/{email}"
        subject = "user verification for three-unicorns url-shortner service"
        to = [email]
        print("sending email....")
        self.send_email(msg=msg, to=to, subject=subject)
        print("email sent successfully....")

    def send_email(self, *, msg, to, subject):
        email = Email()
        email.login()
        body = email.create_msg(message_text=msg, to=to, subject=subject)
        email.send_msg(message=body)

    def get_otp(self):
        digits = "0123456789"
        OTP = ""
        for i in range(6):
            OTP += digits[math.floor(random.random() * 10)]
        return OTP