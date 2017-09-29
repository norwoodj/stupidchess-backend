#!/usr/local/bin/python
from urllib.parse import urlparse, urljoin
from flask import Blueprint, request, jsonify, current_app, abort
from flask_login import login_user, current_user, login_required, logout_user, fresh_login_required
from . import LOGGER

auth_blueprint = Blueprint("auth", __name__)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


@auth_blueprint.route("/", methods=["GET"])
def get_current_user():
    if current_user.is_authenticated:
        return jsonify({
            "id": current_user.get_id(),
            "username": current_user.username,
        })

    abort(404)


@auth_blueprint.route("/", methods=["POST"])
def create_user():
    username, password = request.json.get("username"), request.json.get("password")

    if None in {username, password}:
        return jsonify(message="'username' and 'password' must be provided in request!"), 400

    user = current_app.context.user_service.create_user(username, password)
    login_user(user)
    return jsonify(message="Successfully created user {}".format(username)), 201


@auth_blueprint.route("/login", methods=["POST"])
def login():
    username, password = request.json.get("username"), request.json.get("password")
    remember_me = request.json.get("rememberMe", False)

    if None in {username, password}:
        return jsonify(message="'username' and 'password' must be provided in request!"), 400

    user = current_app.context.user_service.get_user_with_credentials(username, password)

    if user is None:
        LOGGER.debug(f"Invalid login provided for user '{username}'")
        return jsonify(message="Invalid username or password"), 401

    login_user(user, remember=remember_me)
    LOGGER.debug(f"Successfully logged in user '{username}'")
    return jsonify(message="Logged in successfully")


@auth_blueprint.route("/change-password", methods=["POST"])
@fresh_login_required
def change_password():
    username, password, new_password = (
        request.json.get("username"),
        request.json.get("password"),
        request.json.get("newPassword"),
    )

    if None in {username, password, new_password}:
        return jsonify(message="'username' and 'password' and 'newPassword' must be provided in request!"), 400

    user = current_app.context.user_service.get_user_with_credentials(username, password)

    if user is None:
        LOGGER.debug(f"Invalid login provided for user '{username}'")
        return jsonify(message="Invalid username or password"), 401

    current_app.context.user_service.update_user_password(username, new_password)
    return jsonify(message=f"Successfully changed password for user '{username}'")


@auth_blueprint.route("/logout", methods=["POST"])
@login_required
def logout():
    LOGGER.debug(f"Successfully logged out user '{current_user.username}'")
    logout_user()
    return jsonify(message="Logged out successfully")
