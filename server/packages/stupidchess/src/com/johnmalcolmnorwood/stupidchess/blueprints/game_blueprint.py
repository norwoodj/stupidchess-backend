#!/usr/local/bin/python
from flask import Blueprint, request, current_app, jsonify
from flask_login import login_required, current_user

from ..models.move import Move
from ..utils.game_utils import get_game_dict, get_move_dict

game_blueprint = Blueprint("game", __name__)


@game_blueprint.route("/active")
@login_required
def get_active_games():
    game_type = request.args.get("gameType")
    skip = int(request.args.get("skip", 0))
    results = int(request.args.get("results", 10))

    games = current_app.context.game_service.get_active_games_for_user(
        user_uuid=current_user.get_id(),
        game_type=game_type,
        skip=skip,
        results=results,
    )

    return jsonify([get_game_dict(g, current_user.get_id()) for g in games[skip:skip+results]])


@game_blueprint.route("/completed")
@login_required
def get_completed_games():
    user_uuid = request.args.get("userUuid") or current_user.get_id()
    game_type = request.args.get("gameType")
    skip = int(request.args.get("skip", 0))
    results = int(request.args.get("results", 10))

    games = current_app.context.game_service.get_completed_games_for_user(
        user_uuid=user_uuid,
        game_type=game_type,
        skip=skip,
        results=results,
    )

    return jsonify([get_game_dict(g, user_uuid) for g in games[skip:skip+results]])


@game_blueprint.route("/<game_uuid>")
@login_required
def get_game_by_uuid(game_uuid):
    game = current_app.context.game_service.get_game_for_user_and_game_uuid(current_user.get_id(), game_uuid)
    game_dict = get_game_dict(game, current_user.get_id())
    return jsonify(game_dict)


@game_blueprint.route("/<game_uuid>/move/", methods=["POST"])
@login_required
def post_move_to_game(game_uuid):
    move = Move.from_json(request.json)
    move.disambiguating_capture = request.json.get("disambiguatingCapture")
    moves_applied = current_app.context.move_application_service.apply_move(move, game_uuid)

    return jsonify(
        moves=[get_move_dict(m) for m in moves_applied],
        message=f"Successfully made move{'s' if len(moves_applied) > 1 else ''}",
    ), 201


@game_blueprint.route("/<game_uuid>/move/possible")
@login_required
def get_possible_moves(game_uuid):
    if "square" not in request.args:
        return jsonify(message="Must supply 'square' query parameter to get possible moves from that square"), 400

    square = int(request.args.get("square"))
    possible_moves = current_app.context.game_service.get_possible_moves(current_user.get_id(), game_uuid, square)
    ambiguous_moves = current_app.context.ambiguous_move_service.get_ambiguous_moves(possible_moves)

    response_body = {
        "possibleMoves": [
            m.to_dict("startSquare", "destinationSquare", "captures.color", "captures.type", "captures.square")
            for m in possible_moves
        ],
        "ambiguousMoves": ambiguous_moves,
    }

    return jsonify(response_body)
