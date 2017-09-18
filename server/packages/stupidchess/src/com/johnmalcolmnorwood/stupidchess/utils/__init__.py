#!/usr/local/bin/python
from flask import jsonify
from com.johnmalcolmnorwood.stupidchess.utils.game_rules import get_game_scores


def get_game_dict(game):
    game_dict = game.to_dict(
        "_id",
        "type",
        "lastMove",
        "pieces.color", "pieces.type", "pieces.square",
        "captures.color", "captures.type",
        "currentTurn",
        "possiblePiecesToBePlaced",
        "squaresToBePlaced",
        "blackPlayerName",
        "whitePlayerName",
    )

    game_dict["blackPlayerScore"], game_dict["whitePlayerScore"] = get_game_scores(game)
    return game_dict
