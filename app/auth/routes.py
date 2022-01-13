from .src.api.signup import SignupApi
from .src.api.login import LoginApi
from .src.api.user_verification import UserVerification
from .src.api.get_dev_key import GetDevKey

def initialize_routes(api):
    api.add_resource(SignupApi, '/auth/signup')
    api.add_resource(LoginApi, '/auth/login')
    api.add_resource(UserVerification, '/auth/verify')
    api.add_resource(GetDevKey, '/auth/get_dev_key')
