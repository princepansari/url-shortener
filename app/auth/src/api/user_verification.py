from flask import request
from flask_restful import Resource
from app.auth.src.common.utilities import Utils
from app.auth.src.common.rds import RDS
from schema import Schema, And, Use
import bleach

class UserVerification(Resource):

    def __init__(self):
        self.rds = RDS()
        self.schema = Schema({
            'otp': And(int, lambda otp: 000000 <= otp <= 999999)
        }, ignore_extra_keys=True)
    def post(self):
        data = self.schema.validate(request.get_json())
        email = request.args.get('email')
        verified =  self.check_otp(given_otp=data['otp'], email=email)
        if not verified:
            return {'error': 'Wrong OTP'}, 401 #TODO: check http status cde
        self.rds.update_verification_status(email=email)

    def check_otp(self, *, given_otp, email):
        user = self.rds.get_user(email=email)
        valid_otp = self.rds.get_user_otp(user_id=user['user_id'])
        print(valid_otp, "given_otp= ", given_otp)
        return valid_otp == given_otp