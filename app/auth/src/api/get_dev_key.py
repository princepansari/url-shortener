from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from app.common.rds import RDS
import hashlib
import base64
from app.common.config import Config
from http import HTTPStatus


class GetDevKey(Resource):
    def __init__(self):
        self.rds = RDS()
        self.DEVELOPER_KEY_GEN_SECRET = Config.DEVELOPER_KEY_GEN_SECRET

    @jwt_required()
    def get(self):
        email = get_jwt_identity()
        user = self.rds.get_user(email=email)
        developer_key = self.get_developer_key(email=email)
        developer_key_hash = self.hash(input=developer_key)
        self.rds.upsert_dev_key(user_id=user['user_id'],
                                developer_key=developer_key_hash)
        return {'developer_key': developer_key}, HTTPStatus.OK

    def get_developer_key(self, *, email):
        hashed_key = self.hash(input=email + self.DEVELOPER_KEY_GEN_SECRET)
        developer_key = base64.b64encode(hashed_key.encode("ascii")).decode("ascii")
        return developer_key

    def hash(self, *, input):
        return hashlib.sha256(input.encode()).hexdigest()
