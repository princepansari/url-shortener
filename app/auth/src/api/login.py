from flask import request
from flask_jwt_extended import create_access_token
from flask_bcrypt import check_password_hash
from flask_restful import Resource

from app.common.config import Config
from app.common.utilities import Utils
from app.common.rds import RDS
from schema import Schema, And, Use
from http import HTTPStatus
import bleach
import datetime


class LoginApi(Resource):
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
        password = data['password']
        user = self.rds.get_user(email=email)

        if not user:
            return {'error': 'Email or password invalid'}, HTTPStatus.BAD_REQUEST

        if not user['verified']:
            return {'error': 'User verification not completed'}, HTTPStatus.BAD_REQUEST

        password_hash = user['password']
        authorized = self.check_password(password_hash=password_hash, password=password)

        if not authorized:
            return {'error': 'Email or password invalid'}, HTTPStatus.BAD_REQUEST

        self.rds.update_last_login(email=user['email'])
        expires = datetime.timedelta(days=Config.EXPIRE_AFTER_DAYS)
        access_token = create_access_token(identity=str(user['email']), expires_delta=expires)
        return {'token': access_token}, HTTPStatus.OK

    def check_password(self, password_hash, password):
        return check_password_hash(password_hash, password)
