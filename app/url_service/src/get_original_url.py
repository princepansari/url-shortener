from flask import redirect
from flask_restful import Resource
from http import HTTPStatus
from app.common.rds import RDS
from schema import Schema, And, Use
import bleach


class GetOriginalUrl(Resource):
    def __init__(self):
        self.rds = RDS()
        self.schema = Schema(And(str, Use(bleach.clean)))

    def get(self, shortened_link):
        if not self.schema.is_valid(shortened_link):
            return {'error': 'Invalid payload'}, HTTPStatus.BAD_REQUEST
        shortened_link = self.schema.validate(shortened_link)
        original_link = self.rds.get_original_link(shortened_link=shortened_link)
        if original_link is None:
            # TODO - change the json output to the html page for invalid link
            return {'error': 'Invalid shortened link'}, HTTPStatus.BAD_REQUEST
        return redirect(original_link, code=302)


class GetOriginalUrlDev(Resource):
    def __init__(self):
        self.rds = RDS()
        self.schema = Schema(And(str, Use(bleach.clean)))

    def get(self, shortened_link):
        if not self.schema.is_valid(shortened_link):
            return {'error': 'Invalid payload'}, HTTPStatus.BAD_REQUEST
        shortened_link = self.schema.validate(shortened_link)
        original_link = self.rds.get_original_link(shortened_link=shortened_link)
        if original_link is None:
            return {'error': 'Invalid shortened link'}, HTTPStatus.BAD_REQUEST
        return {'original_link': original_link}, HTTPStatus.OK
