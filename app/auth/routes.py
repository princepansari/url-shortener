from .src.api.signup import SignupApi
from .src.api.login import LoginApi


def initialize_routes(api):
    api.add_resource(SignupApi, '/auth/signup')
    api.add_resource(LoginApi, '/auth/login')
