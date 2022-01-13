from flask import request
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.common.rds import RDS


class DeleteUrl(Resource):
    def __init__(self):
        self.rds = RDS()

    @jwt_required()
    def delete(self):
        email = get_jwt_identity()
        data = request.get_json()
        shortened_link = data['shortened_link']

        user_id = self.rds.get_user_by_email(email=email)
        return UtilsDelete.delete_shortened_link(rds=self.rds,
                                                 user_id=user_id,
                                                 shortened_link=shortened_link)


class DeleteUrlDev(Resource):
    def __init__(self):
        self.rds = RDS()

    def delete(self):
        data = request.get_json()
        developer_key = data['developer_key']
        shortened_link = data['shortened_link']

        user_id = self.rds.get_user_by_key(developer_key=developer_key)
        if user_id is None:
            return {'error': 'Invalid user'}, HTTPStatus.UNAUTHORIZED
        return UtilsDelete.delete_shortened_link(rds=self.rds,
                                                 user_id=user_id,
                                                 shortened_link=shortened_link)


class UtilsDelete:

    @staticmethod
    def delete_shortened_link(*, rds, user_id, shortened_link):
        count = rds.delete_shortened_link(user_id=user_id,
                                          shortened_link=shortened_link)
        if count == 0:
            return {'error': 'Invalid shortened link'}, HTTPStatus.BAD_REQUEST
        return {'result': 'URL Removed'}, HTTPStatus.OK
