#!/usr/local/bin/python
from flask import Blueprint, request, current_app, jsonify
from flask_login import login_required, current_user
from .. import LOGGER
from ..models.move import Move
from ..models.game import GameType, GameAuthType
from ..utils import get_game_dict

game_blueprint = Blueprint("game", __name__)


@game_blueprint.route("/types")
def get_game_types():
    return jsonify([
        GameType.STUPID_CHESS,
        GameType.CHESS,
        GameType.CHECKERS,
    ])


@game_blueprint.route("/auth-types")
def get_game_auth_types():
    return jsonify([
        GameAuthType.ONE_PLAYER,
        GameAuthType.TWO_PLAYER,
    ])


@game_blueprint.route("/", methods=["POST"])
@login_required
def post_game():
    LOGGER.debug(f"New game requested with body {request.json}")

    game_type = request.json.get("type")
    game_auth_type = request.json.get("gameAuthType")
    other_player = request.json.get("otherPlayer")

    if None in (game_type, game_auth_type, other_player):
        return jsonify(message="Fields 'otherPlayer', 'type', and 'auth_type' are required!"), 400

    game = current_app.context.game_service.create_game(game_type, game_auth_type, other_player)

    return jsonify(
        message="Successfully created game",
        gameUuid=game.get_id(),
    ), 201


@game_blueprint.route("/")
@login_required
def get_games():
    skip = int(request.args.get("skip", 0))
    results = int(request.args.get("results", 10))
    games = current_app.context.game_service.get_games_for_user(current_user.get_id(), skip=skip, results=results)
    return jsonify([get_game_dict(g) for g in games])


@game_blueprint.route("/<game_uuid>")
@login_required
def get_game_by_uuid(game_uuid):
    game = current_app.context.game_service.get_game_for_user_and_game_uuid(current_user.get_id(), game_uuid)
    game_dict = get_game_dict(game)
    return jsonify(game_dict)


@game_blueprint.route("/<game_uuid>/move/", methods=["POST"])
@login_required
def post_move_to_game(game_uuid):
    move = Move.from_json(request.json)
    move.disambiguating_capture = request.json.get("disambiguatingCapture")
    current_app.context.move_application_service.apply_move(move, game_uuid)

    return jsonify(message="Successfully made move"), 201


def get_possible_move_json_element(possible_move):
    return {
        "captures": [{"color": c.color, "type": c.type, "square": c.square} for c in possible_move.captures or []],
        "startSquare": possible_move.startSquare,
        "destinationSquare": possible_move.destinationSquare,
    }


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
