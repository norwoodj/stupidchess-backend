#!/usr/local/bin/python
from flask import Blueprint, request, current_app, jsonify
from flask_login import login_required, current_user

record_blueprint = Blueprint("record", __name__)


@record_blueprint.route("/")
@login_required
def get_user_records():
    user_uuid = request.args.get("userUuid", current_user.get_id())
    game_type = request.args.get("gameType")

    return jsonify(current_app.context.record_service.get_user_records(user_uuid, game_type))

