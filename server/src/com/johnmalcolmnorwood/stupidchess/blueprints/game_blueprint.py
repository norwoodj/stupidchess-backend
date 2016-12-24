#!/usr/local/bin/python
from flask import Blueprint, request, current_app, jsonify
from com.johnmalcolmnorwood.stupidchess.factories.game_factory import get_new_game_for_game_type
from com.johnmalcolmnorwood.stupidchess.models.move import Move
from com.johnmalcolmnorwood.stupidchess.models.game import Game, GameType, GameAuthType
from com.johnmalcolmnorwood.stupidchess.utils import make_api_response, get_game_dict


game_blueprint = Blueprint('game', __name__)


@game_blueprint.route('/', methods=['POST'])
def post_game():
    game_request = request.json
    game = get_new_game_for_game_type(game_request['type'])

    if game is None:
        return make_api_response(400, 'Invalid game type "{}"')

    game.save()
    return make_api_response(
        status=201,
        message='Successfully created game',
        gameUuid=game.get_id(),
    )


@game_blueprint.route('/')
def get_games():
    games = Game.objects.exclude('createTimestamp', 'lastUpdateTimestamp')
    return jsonify(list(map(get_game_dict, games)))


@game_blueprint.route('/types')
def get_game_types():
    return jsonify([
        GameType.STUPID_CHESS,
        GameType.CHESS,
        GameType.CHECKERS,
    ])


@game_blueprint.route('/auth-types')
def get_game_auth_types():
    return jsonify([
       GameAuthType.ANONYMOUS,
       GameAuthType.SINGLE_PLAYER,
       GameAuthType.TWO_PLAYER,
    ])


@game_blueprint.route('/<game_uuid>')
def get_game_by_uuid(game_uuid):
    game = Game.objects.exclude('createTimestamp', 'lastUpdateTimestamp').get_or_404(_id=game_uuid)
    game_dict = get_game_dict(game)
    return jsonify(game_dict)


@game_blueprint.route('/<game_uuid>/move/', methods=['POST'])
def post_move_to_game(game_uuid):
    move = Move.from_json(request.json)
    move.disambiguating_capture = request.json.get('disambiguatingCapture')
    current_app.context.move_application_service.apply_move(move, game_uuid)

    return make_api_response(
        status=201,
        message='Successfully made move',
    )


def get_possible_move_json_element(possible_move):
    return {
        'captures': [{'color': c.color, 'type': c.type, 'square': c.square} for c in possible_move.captures or []],
        'startSquare': possible_move.startSquare,
        'destinationSquare': possible_move.destinationSquare,
    }


@game_blueprint.route('/<game_uuid>/move/possible')
def get_possible_moves(game_uuid):
    if 'square' not in request.args:
        return make_api_response(400, "Must supply 'square' query parameter to get possible moves from that square")

    square = int(request.args.get('square'))
    possible_moves = current_app.context.possible_move_service.get_possible_moves_from_square(square, game_uuid)
    ambiguous_moves = current_app.context.ambiguous_move_service.get_ambiguous_moves(possible_moves)

    response_body = {
        'possibleMoves': [
            m.to_dict('startSquare', 'destinationSquare', 'captures.color', 'captures.type', 'captures.square')
            for m in possible_moves
        ],
        'ambiguousMoves': ambiguous_moves,
    }

    return jsonify(response_body)
