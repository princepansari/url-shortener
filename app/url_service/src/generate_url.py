from flask import request
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.common.utilities import Utils
from app.common.rds import RDS
from app.common.config import Config
from schema import Schema, And, Use, Optional
import bleach


class GenerateUrl(Resource):
    def __init__(self):
        self.rds = RDS()
        self.schema = Schema({
            'original_link': And(str, Use(bleach.clean), len),
            Optional('custom_alias'): And(str, Utils.validate_custom_alias),
            Optional('expiry_duration'): And(int,
                                             lambda n: Config.MIN_EXPIRY_DURATION <= n <= Config.MAX_EXPIRY_DURATION)
        })

    @jwt_required()
    def post(self):
        email = get_jwt_identity()
        if not self.schema.is_valid(request.get_json()):
            return {'error': 'Invalid payload'}, HTTPStatus.BAD_REQUEST
        data = self.schema.validate(request.get_json())
        original_link = data['original_link']
        custom_alias = data.get('custom_alias')
        expiry_duration = data.get('expiry_duration')
        user_id = self.rds.get_user_by_email(email=email)

        return UtilsURL.get_short_url(rds=self.rds,
                                      user_id=user_id,
                                      original_link=original_link,
                                      custom_alias=custom_alias,
                                      expiry_duration=expiry_duration)


class GenerateUrlDev(Resource):
    def __init__(self):
        self.rds = RDS()
        self.schema = Schema({
            'developer_key': And(str, Use(bleach.clean), len),
            'original_link': And(str, Use(bleach.clean), len),
            Optional('custom_alias'): And(str, Utils.validate_custom_alias),
            Optional('expiry_duration'): And(int,
                                             lambda n: Config.MIN_EXPIRY_DURATION <= n <= Config.MAX_EXPIRY_DURATION)
        })

    def post(self):
        if not self.schema.is_valid(request.get_json()):
            return {'error': 'Invalid payload'}, HTTPStatus.BAD_REQUEST
        data = self.schema.validate(request.get_json())
        developer_key = data['developer_key']
        original_link = data['original_link']
        custom_alias = data.get('custom_alias')
        expiry_duration = data.get('expiry_duration')

        user_id = self.rds.get_user_by_key(developer_key=developer_key)
        if user_id is None:
            return {'error': 'Invalid user'}, HTTPStatus.UNAUTHORIZED

        return UtilsURL.get_short_url(rds=self.rds,
                                      user_id=user_id,
                                      original_link=original_link,
                                      custom_alias=custom_alias,
                                      expiry_duration=expiry_duration)


class UtilsURL:

    @staticmethod
    def get_short_url(*, rds, user_id, original_link, custom_alias, expiry_duration):
        original_link_without_http_and_https = original_link.replace('https://', '').replace('http://', '')
        if original_link_without_http_and_https.startswith(Config.NETLOC1) \
                or original_link_without_http_and_https.startswith(Config.NETLOC2):
            return {'error': 'This domain is banned'}, HTTPStatus.BAD_REQUEST

        if not Utils.is_valid_url(url=original_link):
            return {'error': 'Invalid URL'}, HTTPStatus.BAD_REQUEST

        if custom_alias:
            check = rds.add_shortened_link(user_id=user_id, original_link=original_link,
                                           shortened_link=custom_alias, expiry_duration=expiry_duration)
            if not check:
                return {'error': 'CUSTOM alias already exist!!'}, HTTPStatus.BAD_REQUEST
            shortened_link = custom_alias
        else:
            alias = Utils.encode(url=original_link)
            while not rds.add_shortened_link(user_id=user_id, original_link=original_link,
                                             shortened_link=alias, expiry_duration=expiry_duration):
                alias = Utils.encode(url=original_link)
            shortened_link = alias
        return {'shortened_link': Config.READ_URL + shortened_link}, HTTPStatus.OK
