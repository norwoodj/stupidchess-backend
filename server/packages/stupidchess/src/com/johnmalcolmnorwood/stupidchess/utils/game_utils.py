from .game_rules import get_game_result


def get_game_dict(game, user_uuid):
    game_dict = game.to_dict(
        "type",
        "lastMove",
        "pieces.color", "pieces.type", "pieces.square",
        "captures.color", "captures.type",
        "currentTurn",
        "possiblePiecesToBePlaced",
        "squaresToBePlaced",
        "blackPlayerUuid",
        "whitePlayerUuid",
        "blackPlayerName",
        "whitePlayerName",
        "blackPlayerScore",
        "whitePlayerScore",
        "createTimestamp",
        "lastUpdateTimestamp",
    )

    game_dict["id"] = game.get_id()
    game_dict["createTimestamp"] = game_dict["createTimestamp"].isoformat()
    game_dict["lastUpdateTimestamp"] = game_dict["lastUpdateTimestamp"].isoformat()

    game_dict["gameResult"] = get_game_result(
        game=game,
        user_uuid=user_uuid,
    )

    return game_dict


def get_move_dict(move):
    move_dict = move.to_dict(
        "type",
        "startSquare",
        "destinationSquare",
        "index",
        "piece.color", "piece.type",
        "captures.color", "captures.type",
        "gameUuid",
        "createTimestamp",
        "lastUpdateTimestamp",
    )

    move_dict["id"] = move.get_id()
    move_dict["createTimestamp"] = move_dict["createTimestamp"].isoformat()
    move_dict["lastUpdateTimestamp"] = move_dict["lastUpdateTimestamp"].isoformat()
    return move_dict
