#!/usr/local/bin/python
import base64

from flask import jsonify
from flask_login.login_manager import LoginManager

from . import LOGGER
from .blueprint import auth_blueprint
from .user_service import UserAlreadyExistsException


def create_user_loader(user_service):
    def get_user_by_id(user_id):
        return user_service.get_user_with_id(user_id)

    return get_user_by_id


def create_header_loader(user_service):
    def load_user_from_header(header_val):
        header_val = header_val.replace('Basic ', '', 1)
        header_val = base64.b64decode(header_val).decode('utf-8')
        username, password = header_val.split(':')
        return user_service.get_user_with_credentials(username, password)

    return load_user_from_header


def initialize_authentication(
    app,
    user_service,
    auth_secret_key,
    auth_blueprint_prefix=''
):
    app.secret_key = auth_secret_key
    login_manager = LoginManager(app)
    login_manager.user_loader(create_user_loader(user_service))
    login_manager.header_loader(create_header_loader(user_service))

    LOGGER.debug(f"Registering auth blueprint with prefix {auth_blueprint_prefix}")
    app.register_blueprint(auth_blueprint, url_prefix=auth_blueprint_prefix)

    @app.errorhandler(UserAlreadyExistsException)
    def handle_duplicate_user(error):
        return jsonify(message=f"User {error.username} already exists"), 400
