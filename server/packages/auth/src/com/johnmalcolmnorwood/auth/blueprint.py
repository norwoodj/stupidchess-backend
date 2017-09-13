#!/usr/local/bin/python
from urllib.parse import urlparse, urljoin
from flask import Blueprint, request, jsonify, current_app, abort
from flask_login import login_user, current_user


auth_blueprint = Blueprint('auth', __name__)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


@auth_blueprint.route('/', methods=['GET'])
def get_current_user():
    if current_user.is_authenticated:
        return jsonify({
            "id": current_user.get_id(),
            "username": current_user.username,
        })

    abort(404)


@auth_blueprint.route('/', methods=['POST'])
def create_user():
    username, password = request.json.get('username'), request.json.get('password')

    if None in {username, password}:
        return jsonify(message='"username" and "password" must be provided in request!'), 400

    current_app.context.user_service.create_user(username, password)
    return jsonify(message="Successfully created user {}".format(username)), 201


@auth_blueprint.route('/login', methods=['POST'])
def login():
    username, password = request.json.get('username'), request.json.get('password')

    if None in {username, password}:
        return jsonify(message="'username' and 'password' must be provided in request!"), 400

    user = current_app.context.user_service.get_user_with_credentials(username, password)

    if user is None:
        abort(401)

    login_user(user)
    return jsonify(message='Logged in successfully')
