from flask import request, redirect
from flask_restful import Resource
from http import HTTPStatus
from app.common.rds import RDS
from app.common.config import Config
from app.common.utilities import Utils


class GetOriginalUrl(Resource):
    def __init__(self):
        self.rds = RDS()

    def get(self, shortened_link):
        original_link = self.rds.get_original_link(shortened_link=shortened_link)
        if original_link is None:
            # TODO - change the json output to the html page for invalid link
            return {'error': 'Invalid shortened link'}, HTTPStatus.BAD_REQUEST
        return redirect(original_link, code=302)


class GetOriginalUrlDev(Resource):
    def __init__(self):
        self.rds = RDS()

    def get(self):
        shortened_link = Utils.remove_prefix(request.args['shortened_link'], Config.URL_ENDPOINT)
        if shortened_link is None:
            return {'error': 'Invalid shortened link'}, HTTPStatus.BAD_REQUEST
        original_link = self.rds.get_original_link(shortened_link=shortened_link)
        if original_link is None:
            return {'error': 'Invalid shortened link'}, HTTPStatus.BAD_REQUEST
        return {'original_link': original_link}, HTTPStatus.OK
