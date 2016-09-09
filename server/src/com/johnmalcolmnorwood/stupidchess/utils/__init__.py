#!/usr/local/bin/python
from flask import Response
from com.johnmalcolmnorwood.stupidchess.models.piece import Color
from com.johnmalcolmnorwood.stupidchess.models.game import GameType

SETUP_SQUARES_FOR_COLOR = {
    Color.BLACK: {0, 1, 2, 3, 10, 11, 12, 13, 20, 21, 22, 23},
    Color.WHITE: {94, 95, 96, 97, 104, 105, 106, 107, 114, 115, 116, 117},
}

#STANDARD_CHESS_BOARD = {
#    00, 01, 02, 03, 04, 05, 06, 07,
#    10, 11, 12, 13, 14, 15, 16, 17,
#    20, 21, 22, 23, 24, 25, 26, 27,
#    30, 31, 32, 33, 34, 35, 36, 37,
#    40, 41, 42, 43, 44, 45, 46, 47,
#    50, 51, 52, 53, 54, 55, 56, 57,
#    60, 61, 62, 63, 64, 65, 66, 67,
#    70, 71, 72, 73, 74, 75, 76, 77,
#}

#STUPID_CHESS_BOARD = {
#    000, 001, 002, 003,
#    010, 011, 012, 013,
#    020, 021, 022, 023,
#    030, 031, 032, 033,
#    040, 041, 042, 043, 044, 045, 046, 047,
#    050, 051, 052, 053, 054, 055, 056, 057,
#    060, 061, 062, 063, 064, 065, 066, 067,
#    070, 071, 072, 073, 074, 075, 076, 077,
#                        084, 085, 086, 087,
#                        094, 095, 096, 097,
#                        104, 105, 106, 107,
#                        114, 115, 116, 117,
#}

#BOARD_SQUARES_FOR_GAME_TYPE = {
#    GameType.STUPID_CHESS: STUPID_CHESS_BOARD,
#    GameType.CHESS: STANDARD_CHESS_BOARD,
#    GameType.CHECKERS: STUPID_CHESS_BOARD,
#}

#STUPID_CHESS_MIDDLE_SECTION = {square for square in STUPID_CHESS_BOARD if 40 <= square <= 80}

#BOARD_MIDDLE_SECTION_FOR_GAME_TYPE = {
#    GameType.STUPID_CHESS: STUPID_CHESS_MIDDLE_SECTION,
#    GameType.CHESS: set(),
#    GameType.CHECKERS: set(),
#}

def make_api_response(status, message):
    return Response(
            status=status,
            response={'message': message}
    )
