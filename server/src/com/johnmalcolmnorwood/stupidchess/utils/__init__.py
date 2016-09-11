#!/usr/local/bin/python
import json
from flask import Response
from com.johnmalcolmnorwood.stupidchess.models.piece import Color, Piece
from com.johnmalcolmnorwood.stupidchess.models.game import GameType

SETUP_SQUARES_FOR_COLOR = {
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
    GameType.CHECKERS: STUPID_CHESS_BOARD,
}

STUPID_CHESS_MIDDLE_SECTION = {square for square in STUPID_CHESS_BOARD if 40 <= square <= 80}

BOARD_MIDDLE_SECTION_FOR_GAME_TYPE = {
    GameType.STUPID_CHESS: STUPID_CHESS_MIDDLE_SECTION,
    GameType.CHESS: set(),
    GameType.CHECKERS: set(),
}


def make_api_response(status, message):
    return Response(
            status=status,
            response=json.dumps({'message': message})
    )


def get_piece_for_move_db_object(piece):
    return Piece(
        color=piece.color,
        type=piece.type,
    )

