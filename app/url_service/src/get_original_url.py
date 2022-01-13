from flask import request
from flask_restful import Resource
from http import HTTPStatus
from app.common.rds import RDS


class GetOriginalUrl(Resource):
    def __init__(self):
        self.rds = RDS()

    def get(self):
        shortened_link = request.args['shortened_link']
        original_link = self.rds.get_original_link(shortened_link=shortened_link)
        if original_link is None:
            return {'error': 'Invalid shortened link'}, HTTPStatus.BAD_REQUEST
        return {'original_link': original_link}, HTTPStatus.OK
