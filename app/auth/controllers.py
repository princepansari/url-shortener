# Import flask dependencies
from flask import Blueprint, request, g, redirect

# Define the blueprint: 'auth', set its url prefix: app.url/auth
auth = Blueprint('auth', __name__, url_prefix='/auth')

# Set the route and accepted methods
@auth.route('/signin/', methods=['GET', 'POST'])
def signin():
    pass
