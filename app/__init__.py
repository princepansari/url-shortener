# Import flask and template operators
from flask import Flask
from flask_restful import  Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from .auth.routes import initialize_routes
from app.url_service.routes import url_service_routes
from app.swagger.routes import initialize_swagger_routes

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

initialize_routes(api)
url_service_routes(api)
initialize_swagger_routes(api)
