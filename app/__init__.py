# Import flask and template operators
from flask import Flask
from flask_restful import  Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from auth.routes import initialize_routes

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

initialize_routes(api)