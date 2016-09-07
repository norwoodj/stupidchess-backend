#!/usr/local/bin/python
from flask import Blueprint, request, Response, current_app
from com.johnmalcolmnorwood.stupidchess.factories.game_factory import GameFactory
from com.johnmalcolmnorwood.stupidchess.models.move import Move

game_blueprint = Blueprint('game', __name__)


@game_blueprint.route('/', methods=['POST'])
def post_game():
    game_request = request.json
    game = GameFactory.get_new_game_for_game_type(game_request['type'])

    if game is None:
        return Response(status=400, response={'message': 'Invalid game type "{}"'.format(game_request['type'])})

    game.save()
    return Response(status=201, response={'message': 'Saved new game'})


@game_blueprint.route('/')
def get_games():
    context = current_app.cxt
    return context.game_service.find().to_json()


@game_blueprint.route('/<game_uuid>')
def get_game_by_uuid(game_uuid):
    context = current_app.cxt
    game = context.game_service.find_one(_id=game_uuid)
    return Response(response=game.to_json(), status=200, content_type='application/json')


@game_blueprint.route('/<game_uuid>/move/', methods=['POST'])
def post_move_to_game(game_uuid):
    context = current_app.cxt
    move = Move.from_json(request.json['move'])
    context.move_service.apply_move(move, game_uuid)

    return Response(response='Done', status=200, content_type='application/json')
