#!/usr/local/bin/python
from com.johnmalcolmnorwood.stupidchess.models.game import Game, GameType
from com.johnmalcolmnorwood.stupidchess.models.piece import Piece, Color, PieceType


def get_new_game_for_game_type(game_type):
    return GAME_TYPE_TO_CREATE_FUNCTION.get(game_type, lambda: None)()


STUPID_CHESS_INTIAL_SQUARES_TO_BE_PLACED = [
    0, 1, 2, 3,
    10, 11, 12, 13,
    20, 21, 22, 23,
    94, 95, 96, 97,
    104, 105, 106, 107,
    114, 115, 116, 117,
]

STUPID_CHESS_INTIAL_PIECES_FOR_SIDE = [
    PieceType.KING,
    PieceType.QUEEN,
    PieceType.BISHOP,
    PieceType.BISHOP,
    PieceType.CASTLE,
    PieceType.CASTLE,
    PieceType.PONY,
    PieceType.CHECKER,
    PieceType.PAWN,
    PieceType.PAWN,
    PieceType.PAWN,
    PieceType.PAWN,
]

STUPID_CHESS_INITIAL_PIECES_TO_BE_PLACED = [
    Piece(type=piece_type, color=color, index=idx)
    for idx, piece_type in enumerate(STUPID_CHESS_INTIAL_PIECES_FOR_SIDE) for color in (Color.BLACK, Color.WHITE)
]


def get_new_stupid_chess_game():
    return Game(
        type=GameType.STUPID_CHESS,
        possiblePiecesToBePlaced=STUPID_CHESS_INITIAL_PIECES_TO_BE_PLACED,
        squaresToBePlaced=STUPID_CHESS_INTIAL_SQUARES_TO_BE_PLACED,
        currentTurn=Color.BLACK,
        blackScore=1,
        whiteScore=1,
    )


GAME_TYPE_TO_CREATE_FUNCTION = {
    GameType.STUPID_CHESS: get_new_stupid_chess_game,
}
