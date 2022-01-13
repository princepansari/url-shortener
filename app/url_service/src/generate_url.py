from flask import  request
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
import validators
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common.utilities import Utils
from common.rds import RDS


class GenerateUrl(Resource):
    def __init__(self):
        self.rds = RDS()

    @jwt_required()
    def post(self):
        email = get_jwt_identity()
        # TODO: CHECK KEY
        data = request.get_json()
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

    def post(self):
        # TODO: CHECK KEY
        data = request.get_json()
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
        if not validators.url(original_link):
            return {'error': 'Invalid URL'}, HTTPStatus.BAD_REQUEST

        if custom_alias:
            exist = rds.is_shortened_link_exists(shortened_link=custom_alias)
            if exist:
                return {'error': 'CUSTOM alias already exist!!'}, HTTPStatus.BAD_REQUEST
            shortened_link = custom_alias
        else:
            alias = Utils.encode(url=original_link)
            while rds.is_shortened_link_exists(shortened_link=alias):
                alias = Utils.encode(url=original_link)
            shortened_link = alias

        rds.add_shortened_link(user_id=user_id,
                               original_link=original_link,
                               shortened_link=shortened_link,
                               expiry_duration=expiry_duration)
        return {'shortened_link': shortened_link}, HTTPStatus.OK
