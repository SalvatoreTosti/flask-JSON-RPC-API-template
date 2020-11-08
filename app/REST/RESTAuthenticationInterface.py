from flask import g, make_response, jsonify
from flask_login import current_user, login_required
from flask_httpauth import HTTPBasicAuth
from app import app
from app.models.user import User
from app.REST.utils import api_base_url

auth = HTTPBasicAuth()

base_url = api_base_url


@auth.verify_password
def verify_password(username_or_token, password=None):
    user = User.verify_auth_token(username_or_token)
    if not user:
        user = User.query.filter_by(username=str(username_or_token)).first()
        if not user or not user.check_password(password):
            return False
    g.user = user
    return True


@auth.error_handler
def unauthorized():
    return make_response(jsonify({"error": "Unauthorized access"}), 401)


# This route is designed to allow front-end authenticated user sessions to obtain an API token
@app.route(base_url + "/token")
@login_required
def get_auth_token():
    token = current_user.generate_auth_token()
    return jsonify({"token": token.decode("ascii")})


@app.route(base_url + "/generate-token")
@auth.login_required
def generate_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({"token": token.decode("ascii")})
