# Import flask and template operators
from flask import Flask
from flask_restful import  Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from .auth.routes import initialize_routes
from app.url_service.routes import url_service_routes
from app.swagger.routes import initialize_swagger_routes
from flask_cors import CORS
import logging
import faulthandler
faulthandler.enable()

print("====================in init.py========================")


# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

api = Api(app)
cors = CORS(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

initialize_routes(api)
url_service_routes(api)
initialize_swagger_routes(api)

gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.DEBUG)
app.logger.debug('from app/__init__.py | this will show in the log|================')
