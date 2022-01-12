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


class GetOriginalUrl(Resource):
    def __init__(self):
        self.rds = RDS()

    # @jwt_required
    def get(self):
        # email = "princep@iitbhilai.ac.in"
        # email = get_jwt_identity()
        pass


class GetOriginalUrlDev(Resource):
    def __init__(self):
        self.rds = RDS()

    def get(self):
        data = request.get_json()
        developer_key = data['developer_key']
        shortened_link = data['shortened_link']

        pass
