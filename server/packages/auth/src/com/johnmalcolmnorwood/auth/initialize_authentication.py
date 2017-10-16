#!/usr/local/bin/python
import base64

from flask import request, url_for, redirect
from flask_login.login_manager import LoginManager

from . import LOGGER
from .auth_blueprint import auth_blueprint
from .utils import NEXT_QUERY_PARAM_PREFIX


def create_user_loader(user_service):
    def get_user_by_id(user_id):
        return user_service.get_user_with_id(user_id)

    return get_user_by_id


def create_header_loader(user_service):
    def load_user_from_header(header_val):
        header_val = header_val.replace("Basic ", "", 1)
        header_val = base64.b64decode(header_val).decode("utf-8")
        username, password = header_val.split(":")
        return user_service.get_user_with_credentials(username, password)

    return load_user_from_header


def handle_unauthorized():
    next_path = request.endpoint
    next_args = {f"{NEXT_QUERY_PARAM_PREFIX}{k}": v for k, v in request.args.items()}
    return redirect(url_for("auth.login", next=next_path, **next_args))


def initialize_authentication(
    app,
    user_service,
    auth_secret_key,
    auth_blueprint_prefix="",
    login_view=None,
):
    app.secret_key = auth_secret_key
    login_manager = LoginManager(app)
    login_manager.user_loader(create_user_loader(user_service))
    login_manager.unauthorized_handler(handle_unauthorized)
    login_manager.header_loader(create_header_loader(user_service))
    login_manager.login_view = login_view

    LOGGER.debug(f"Registering auth blueprint with prefix '{auth_blueprint_prefix}'")
    app.register_blueprint(auth_blueprint, url_prefix=auth_blueprint_prefix)
