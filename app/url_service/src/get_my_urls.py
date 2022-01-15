from flask import request
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.common.rds import RDS
from schema import Schema, And, Use
import bleach


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
        self.schema = Schema({
            'developer_key': And(str,  Use(bleach.clean), len)
        })

    def get(self):
        if not self.schema.is_valid(request.args.to_dict()):
            return {'error': 'Invalid payload'}, HTTPStatus.BAD_REQUEST
        data = self.schema.validate(request.args.to_dict())
        developer_key = data['developer_key']
        user_id = self.rds.get_user_by_key(developer_key=developer_key)
        if user_id is None:
            return {'error': 'Invalid user'}, HTTPStatus.UNAUTHORIZED
        return self.rds.get_user_links(user_id=user_id), HTTPStatus.OK
