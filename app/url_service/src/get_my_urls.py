from flask import request
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common.rds import RDS


class GetMyUrls(Resource):
    def __init__(self):
        self.rds = RDS()

    @jwt_required()
    def get(self):
        email = get_jwt_identity()
        user_id = self.rds.get_user_by_email(email=email)
        return self.rds.get_user_links(user_id=user_id), HTTPStatus.OK


class GetMyUrlsDev(Resource):
    def __init__(self):
        self.rds = RDS()

    def get(self):
        developer_key = request.args['developer_key']
        user_id = self.rds.get_user_by_key(developer_key=developer_key)
        if user_id is None:
            return {'error': 'Invalid user'}, HTTPStatus.UNAUTHORIZED
        return self.rds.get_user_links(user_id=user_id), HTTPStatus.OK
