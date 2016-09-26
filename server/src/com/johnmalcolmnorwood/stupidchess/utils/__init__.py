#!/usr/local/bin/python
from flask import jsonify
from com.johnmalcolmnorwood.stupidchess.utils.game_rules import get_game_scores


def make_api_response(status, message, **kwargs):
    return jsonify({'message': message, **kwargs}), status


def get_game_dict(game):
    game_dict = game.to_dict(
        'type',
        'lastMove',
        'pieces.color', 'pieces.type', 'pieces.square',
        'captures.color', 'captures.type',
        'currentTurn',
        'possiblePiecesToBePlaced',
        'squaresToBePlaced',
    )

    game_dict['blackScore'], game_dict['whiteScore'] = get_game_scores(game)
    return game_dict
