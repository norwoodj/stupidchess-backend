#!/usr/local/bin/python
from flask import Blueprint, request, current_app, jsonify
from flask_login import login_required, current_user
from ..models.move import Move
from ..utils.game_utils import get_game_dict, get_move_dict, LIST_GAME_DICT_FIELDS, SINGLE_GAME_DICT_FIELDS

game_blueprint = Blueprint("game", __name__)


DEFAULT_PAGE_OFFSET = 0
DEFAULT_PAGE_LIMIT = 10


def _get_page_query_parameters():
    return int(request.args.get("offset", DEFAULT_PAGE_OFFSET)), int(request.args.get("limit", DEFAULT_PAGE_LIMIT))


def _retrieve_game_list(one_player_retrieval_method, two_player_retrieval_method):
    user_uuid = request.args.get("userUuid") or current_user.get_id()
    game_type = request.args.get("gameType")
    offset, limit = _get_page_query_parameters()

    if user_uuid == current_user.get_id():
        games = one_player_retrieval_method(
            user_uuid=user_uuid,
            game_type=game_type,
            offset=offset,
            limit=limit,
        )
    else:
        games = two_player_retrieval_method(
            user_one_uuid=current_user.get_id(),
            user_two_uuid=user_uuid,
            game_type=game_type,
            offset=offset,
            limit=limit,
        )

    return jsonify([get_game_dict(g, user_uuid, LIST_GAME_DICT_FIELDS) for g in games])


def _retrieve_game_count(one_player_retrieval_method, two_player_retrieval_method):
    user_uuid = request.args.get("userUuid") or current_user.get_id()
    game_type = request.args.get("gameType")

    if user_uuid == current_user.get_id():
        count = one_player_retrieval_method(
            user_uuid=user_uuid,
            game_type=game_type,
        )
    else:
        count = two_player_retrieval_method(
            user_one_uuid=current_user.get_id(),
            user_two_uuid=user_uuid,
            game_type=game_type,
        )

    return jsonify(gameCount=count)


@game_blueprint.route("/active")
@login_required
def get_active_games():
    return _retrieve_game_list(
        current_app.context.game_service.get_active_games_for_user,
        current_app.context.game_service.get_active_games_for_users,
    )


@game_blueprint.route("/active/count")
@login_required
def count_active_games():
    return _retrieve_game_count(
        current_app.context.game_service.count_active_games_for_user,
        current_app.context.game_service.count_active_games_for_users,
    )


@game_blueprint.route("/completed")
@login_required
def get_completed_games():
    return _retrieve_game_list(
        current_app.context.game_service.get_completed_games_for_user,
        current_app.context.game_service.get_completed_games_for_users,
    )


@game_blueprint.route("/completed/count")
@login_required
def count_completed_games():
    return _retrieve_game_count(
        current_app.context.game_service.count_completed_games_for_user,
        current_app.context.game_service.count_completed_games_for_users,
    )


@game_blueprint.route("/<game_uuid>")
@login_required
def get_game_by_uuid(game_uuid):
    game = current_app.context.game_service.get_game_for_user_and_game_uuid(current_user.get_id(), game_uuid)
    game_dict = get_game_dict(game, current_user.get_id(), SINGLE_GAME_DICT_FIELDS)
    return jsonify(game_dict)


@game_blueprint.route("/<game_uuid>/move")
@login_required
def get_moves_for_game(game_uuid):
    offset, limit = _get_page_query_parameters()
    moves = current_app.context.move_service.get_moves_for_game_and_user(game_uuid, current_user.get_id(), offset, limit)
    return jsonify([get_move_dict(m) for m in moves])


@game_blueprint.route("/<game_uuid>/move/count")
@login_required
def count_moves_for_game(game_uuid):
    count = current_app.context.move_service.count_moves_for_game_and_user(game_uuid, current_user.get_id())
    return jsonify(moveCount=count)


@game_blueprint.route("/<game_uuid>/move/", methods=["POST"])
@login_required
def post_move_to_game(game_uuid):
    move = Move.from_json(request.json)
    move.disambiguating_capture = request.json.get("disambiguatingCapture")
    moves_applied = current_app.context.move_service.apply_move(current_user.get_id(), game_uuid, move)

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
    possible_moves = current_app.context.possible_move_service.get_possible_moves_from_square(
        square=square,
        game_uuid=game_uuid,
        user_uuid=current_user.get_id(),
    )

    ambiguous_moves = current_app.context.ambiguous_move_service.get_ambiguous_moves(possible_moves)

    response_body = {
        "possibleMoves": [
            m.to_dict("startSquare", "destinationSquare", "captures.color", "captures.type", "captures.square")
            for m in possible_moves
        ],
        "ambiguousMoves": ambiguous_moves,
    }

    return jsonify(response_body)
