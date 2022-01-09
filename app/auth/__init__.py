# Import flask and template operators
from flask import Flask

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

from app.auth.controllers import auth as auth_module

# Register blueprint(s)
app.register_blueprint(auth_module)
# app.register_blueprint(xyz_module)
# ..
