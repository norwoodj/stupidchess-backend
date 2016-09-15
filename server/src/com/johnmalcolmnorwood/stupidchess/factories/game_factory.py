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
    PieceType.PAWN,
    PieceType.PAWN,
    PieceType.PAWN,
    PieceType.PAWN,
    PieceType.PONY,
    PieceType.CHECKER,
    PieceType.CASTLE,
    PieceType.CASTLE,
    PieceType.BISHOP,
    PieceType.BISHOP,
    PieceType.QUEEN,
    PieceType.KING,
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

CHESS_INITIAL_PIECES = [
    Piece(type=PieceType.KING, color=Color.BLACK, square=4),
    Piece(type=PieceType.QUEEN, color=Color.BLACK, square=3),
    Piece(type=PieceType.BISHOP, color=Color.BLACK, square=2),
    Piece(type=PieceType.BISHOP, color=Color.BLACK, square=5),
    Piece(type=PieceType.PONY, color=Color.BLACK, square=1),
    Piece(type=PieceType.PONY, color=Color.BLACK, square=6),
    Piece(type=PieceType.CASTLE, color=Color.BLACK, square=0),
    Piece(type=PieceType.CASTLE, color=Color.BLACK, square=7),
    *[Piece(type=PieceType.PAWN, color=Color.BLACK, square=square) for square in range(10, 18)],

    Piece(type=PieceType.KING, color=Color.WHITE , square=74),
    Piece(type=PieceType.QUEEN, color=Color.WHITE, square=73),
    Piece(type=PieceType.BISHOP, color=Color.WHITE, square=72),
    Piece(type=PieceType.BISHOP, color=Color.WHITE, square=75),
    Piece(type=PieceType.PONY, color=Color.WHITE, square=71),
    Piece(type=PieceType.PONY, color=Color.WHITE, square=76),
    Piece(type=PieceType.CASTLE, color=Color.WHITE, square=70),
    Piece(type=PieceType.CASTLE, color=Color.WHITE, square=77),
    *[Piece(type=PieceType.PAWN, color=Color.WHITE, square=square) for square in range(60, 68)],
]


def get_new_chess_game():
    return Game(
        type=GameType.CHESS,
        pieces=CHESS_INITIAL_PIECES,
        currentTurn=Color.WHITE,
        blackScore=1,
        whiteScore=1,
    )

CHECKERS_INITIAL_PIECES = [
    *[Piece(type=PieceType.CHECKER, color=Color.BLACK, square=square) for square in range(0, 8, 2)],
    *[Piece(type=PieceType.CHECKER, color=Color.BLACK, square=square) for square in range(11, 18, 2)],
    *[Piece(type=PieceType.CHECKER, color=Color.BLACK, square=square) for square in range(20, 28, 2)],

    *[Piece(type=PieceType.CHECKER, color=Color.WHITE, square=square) for square in range(51, 58, 2)],
    *[Piece(type=PieceType.CHECKER, color=Color.WHITE, square=square) for square in range(60, 68, 2)],
    *[Piece(type=PieceType.CHECKER, color=Color.WHITE, square=square) for square in range(71, 78, 2)],
]


def get_new_checkers_game():
    return Game(
        type=GameType.CHECKERS,
        pieces=CHECKERS_INITIAL_PIECES,
        currentTurn=Color.WHITE,
        blackScore=sum(1 for _ in filter(lambda piece: piece.color == Color.BLACK, CHECKERS_INITIAL_PIECES)),
        whiteScore=sum(1 for _ in filter(lambda piece: piece.color == Color.WHITE, CHECKERS_INITIAL_PIECES)),
    )


GAME_TYPE_TO_CREATE_FUNCTION = {
    GameType.STUPID_CHESS: get_new_stupid_chess_game,
    GameType.CHESS: get_new_chess_game,
    GameType.CHECKERS: get_new_checkers_game,
}

