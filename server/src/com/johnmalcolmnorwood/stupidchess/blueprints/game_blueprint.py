#!/usr/local/bin/python
import json
from flask import Blueprint, request, Response, current_app
from com.johnmalcolmnorwood.stupidchess.factories.game_factory import get_new_game_for_game_type
from com.johnmalcolmnorwood.stupidchess.models.move import Move
from com.johnmalcolmnorwood.stupidchess.models.game import Game
from com.johnmalcolmnorwood.stupidchess.utils import make_api_response

game_blueprint = Blueprint('game', __name__)


@game_blueprint.route('/', methods=['POST'])
def post_game():
    game_request = request.json
    game = get_new_game_for_game_type(game_request['type'])

    if game is None:
        return make_api_response(400, 'Invalid game type "{}"')

    game.save()
    return Response(status=201, response=json.dumps({'gameUuid': game.get_id()}), mimetype='application/json')


@game_blueprint.route('/')
def get_games():
    games = Game.objects.exclude('createTimestamp', 'lastUpdateTimestamp')
    return games.to_json()


@game_blueprint.route('/<game_uuid>')
def get_game_by_uuid(game_uuid):
    game = Game.objects.exclude('createTimestamp', 'lastUpdateTimestamp').get_or_404(_id=game_uuid)
    return Response(response=game.to_json(), status=200, content_type='application/json')


@game_blueprint.route('/<game_uuid>/move/', methods=['POST'])
def post_move_to_game(game_uuid):
    move = Move.from_json(request.json)
    current_app.context.move_application_service.apply_move(move, game_uuid)

    return make_api_response(201, 'Successfully made move')


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
    move_json_response = json.dumps([get_possible_move_json_element(m) for m in possible_moves])

    return Response(response=move_json_response, status=200, content_type='application/json')
