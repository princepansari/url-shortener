import json
from flask import Response, request
from flask_restful import Resource
from http import HTTPStatus
# from flask_jwt_extended import jwt_required

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common.utilities import Utils
from common.rds import RDS


class GenerateURL(Resource):
    def __init__(self):
        self.rds = RDS()

    # @jwt_required
    def post(self):
        email = "princep@iitbhilai.ac.in"
        # email = get_jwt_identity()
        # TODO: CHECK KEY
        data = request.get_json()
        original_link = data['original_link']
        custom_alias = data.get('custom_alias')
        expiry_duration = data.get('expiry_duration')
        user_id = self.rds.get_user_by_email(email=email)

        response = UtilsURL.get_short_url(rds=self.rds,
                                          user_id=user_id,
                                          original_link=original_link,
                                          custom_alias=custom_alias,
                                          expiry_duration=expiry_duration)

        return Response(json.dumps(response), mimetype='application/json', status=HTTPStatus.OK)


class CreateURL(Resource):
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
            return Response(json.dumps({'error': 'Invalid user'}),
                            mimetype='application/json',
                            status=HTTPStatus.BAD_REQUEST)

        response = UtilsURL.get_short_url(rds=self.rds,
                                          user_id=user_id,
                                          original_link=original_link,
                                          custom_alias=custom_alias,
                                          expiry_duration=expiry_duration)
        return Response(json.dumps(response), mimetype='application/json', status=HTTPStatus.OK)


class UtilsURL:

    @staticmethod
    def get_short_url(*, rds, user_id, original_link, custom_alias, expiry_duration):
        if custom_alias:
            exist = rds.check_shortened_link(shortened_link=custom_alias)
            if exist:
                return {'output': 'CUSTOM alias already exist!!'}
            rds.add_alias(user_id=user_id,
                          original_link=original_link,
                          shortened_link=custom_alias,
                          expiry_duration=expiry_duration)
            return {'output': 'CUSTOM alias created', 'short_url': custom_alias}
        else:
            alias = Utils.encode(url=original_link)
            while rds.check_shortened_link(shortened_link=alias):
                alias = Utils.encode(url=original_link)

            rds.add_alias(user_id=user_id,
                          original_link=original_link,
                          shortened_link=alias,
                          expiry_duration=expiry_duration)
            return {'output': 'CUSTOM alias created', 'short_url': alias}
