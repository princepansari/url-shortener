from flask import request
from flask_restful import Resource
from flask_bcrypt import generate_password_hash
from app.auth.src.common.utilities import Utils
from app.auth.src.common.rds import RDS
import os
import hashlib
import base64

class SignupApi(Resource):
    def __init__(self):
        self.rds = RDS()
        self.DEVELOPER_KEY_GEN_SECRET = os.environ.get('DEVELOPER_KEY_GEN_SECRET')

    def post(self):
        data = Utils.sanitize_dict(request.get_json())
        email = data['email']
        password = self.hash_password(data['password'])
        developer_key = self.hash_password(self.get_developer_key(email))
        self.rds.create_user(email=email,
                             password=password,
                             developer_key=developer_key)

    def get_developer_key(self, email):
        hash = hashlib.sha256((email+self.DEVELOPER_KEY_GEN_SECRET).encode()).hexdigest()
        developer_key = base64.b64encode(hash.encode("ascii")).decode("ascii")
        return developer_key

    def hash_password(self, password):
        return generate_password_hash(password).decode('utf8')