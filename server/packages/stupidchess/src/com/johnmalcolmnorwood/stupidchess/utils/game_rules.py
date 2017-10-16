#!/usr/local/bin/python
from ..models.piece import Color, PieceType
from ..models.game import GameType, GameResult


_SETUP_SQUARES_FOR_COLOR = {
    Color.BLACK: {0, 1, 2, 3, 10, 11, 12, 13, 20, 21, 22, 23},
    Color.WHITE: {94, 95, 96, 97, 104, 105, 106, 107, 114, 115, 116, 117},
}

STANDARD_CHESS_BOARD = {
    0, 1, 2, 3, 4, 5, 6, 7,
    10, 11, 12, 13, 14, 15, 16, 17,
    20, 21, 22, 23, 24, 25, 26, 27,
    30, 31, 32, 33, 34, 35, 36, 37,
    40, 41, 42, 43, 44, 45, 46, 47,
    50, 51, 52, 53, 54, 55, 56, 57,
    60, 61, 62, 63, 64, 65, 66, 67,
    70, 71, 72, 73, 74, 75, 76, 77,
}

STUPID_CHESS_BOARD = {
    0, 1, 2, 3,
    10, 11, 12, 13,
    20, 21, 22, 23,
    30, 31, 32, 33,
    40, 41, 42, 43, 44, 45, 46, 47,
    50, 51, 52, 53, 54, 55, 56, 57,
    60, 61, 62, 63, 64, 65, 66, 67,
    70, 71, 72, 73, 74, 75, 76, 77,
    84, 85, 86, 87,
    94, 95, 96, 97,
    104, 105, 106, 107,
    114, 115, 116, 117,
}

BOARD_SQUARES_FOR_GAME_TYPE = {
    GameType.STUPID_CHESS: STUPID_CHESS_BOARD,
    GameType.CHESS: STANDARD_CHESS_BOARD,
    GameType.CHECKERS: STANDARD_CHESS_BOARD,
}

STUPID_CHESS_MIDDLE_SECTION = {square for square in STUPID_CHESS_BOARD if 40 <= square <= 80}

BOARD_MIDDLE_SECTION_FOR_GAME_TYPE = {
    GameType.STUPID_CHESS: STUPID_CHESS_MIDDLE_SECTION,
    GameType.CHESS: set(),
    GameType.CHECKERS: set(),
}

_POSSIBLE_CHESS_PAWN_REPLACEMENTS = [
    PieceType.QUEEN,
    PieceType.CASTLE,
    PieceType.BISHOP,
    PieceType.PONY,
]


def is_king(piece):
    return piece.type in {PieceType.KING, PieceType.CHECKER_KING}


def count(iterable):
    return sum(1 for _ in iterable)


def is_in_board_setup_mode(game):
    return game.type == GameType.STUPID_CHESS and game.lastMove < 23


def is_players_turn(game, user_uuid):
    return any([
        game.blackPlayerUuid == game.whitePlayerUuid,
        game.currentTurn == Color.BLACK and game.blackPlayerUuid == user_uuid,
        game.currentTurn == Color.WHITE and game.whitePlayerUuid == user_uuid,
    ])


def get_pawn_replacement_pieces_for_game_type_and_color(game_type, color):
    chess_replacements = [
        {"color": color, "index": i, "type": t} for i, t in enumerate(_POSSIBLE_CHESS_PAWN_REPLACEMENTS)
    ]

    if game_type == GameType.CHESS:
        return chess_replacements

    if game_type == GameType.STUPID_CHESS:
        return [
            *chess_replacements,
            {"color": color, "index": len(_POSSIBLE_CHESS_PAWN_REPLACEMENTS), "type": PieceType.CHECKER_KING},
        ]


def get_game_result(
    game,
    user_uuid
):
    if 0 not in (game.blackPlayerScore, game.whitePlayerScore):
        return None

    if game.blackPlayerUuid == game.whitePlayerUuid:
        return GameResult.LOSS if game.blackPlayerScore == 0 else GameResult.WIN

    return (
        GameResult.WIN if game.blackPlayerScore == 0 and game.whitePlayerUuid == user_uuid else
        GameResult.WIN if game.whitePlayerScore == 0 and game.blackPlayerUuid == user_uuid else
        GameResult.LOSS
    )


def is_in_piece_promotion_zone(square, game_type, color):
    if color == Color.WHITE and square < 10:
        return True

    if color == Color.BLACK:
        if game_type == GameType.STUPID_CHESS and square > 110:
            return True
        if game_type in (GameType.CHESS, GameType.CHECKERS) and square > 70:
            return True

    return False


def is_square_in_setup_zone_for_color(color, square):
    return square in _SETUP_SQUARES_FOR_COLOR[color]
