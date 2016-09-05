#!/usr/local/bin/python
from flask import Blueprint, request, Response
from com.johnmalcolmnorwood.stupidchess.models.game import Game
from com.johnmalcolmnorwood.stupidchess.factories.game_factory import GameFactory

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
    return Game.objects.to_json()


@game_blueprint.route('/<game_uuid>')
def get_game_by_uuid(game_uuid):
    game = Game.objects.get_or_404(_id=game_uuid).to_json()
    return Response(response=game, status=200, content_type='application/json')
