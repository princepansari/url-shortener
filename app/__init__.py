# Import flask and template operators
from flask import Flask
from flask_restful import  Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from .auth.routes import initialize_routes
from app.url_service.routes import url_service_routes
from flask_cors import CORS

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