from flask import request
from flask_jwt_extended import create_access_token
from flask_bcrypt import check_password_hash
from flask_restful import Resource
from app.auth.src.common.utilities import Utils
from app.auth.src.common.rds import RDS
import datetime


class LoginApi(Resource):
    def __init__(self):
        self.rds = RDS()

    def post(self):
        data = Utils.sanitize_dict(request.get_json())
        email = data['email']
        password = data['password']
        user = self.rds.get_user(email=email)
        authorized = self.check_password(password_hash=user['password'], password=password)

        if not authorized:
            return {'error': 'Email or password invalid'}, 401

        expires = datetime.timedelta(days=7)
        access_token = create_access_token(identity=str(user['email']), expires_delta=expires)
        return {'token': access_token}, 200

    def check_password(self, password_hash, password):
        return check_password_hash(password_hash, password)
