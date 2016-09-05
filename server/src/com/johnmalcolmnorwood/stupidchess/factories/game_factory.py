#!/usr/local/bin/python
from com.johnmalcolmnorwood.stupidchess.models.game_type import GameType
from com.johnmalcolmnorwood.stupidchess.models.game import Game
from com.johnmalcolmnorwood.stupidchess.models.piece import Piece
from com.johnmalcolmnorwood.stupidchess.models.color import Color
from com.johnmalcolmnorwood.stupidchess.models.piece_type import PieceType


class GameFactory:
    @staticmethod
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

    STUPID_CHESS_INTIAL_PIECES_TO_BE_PLACED = [
        Piece(type=PieceType.KING, color=Color.BLACK),
        Piece(type=PieceType.QUEEN, color=Color.WHITE),
    ]

    @staticmethod
    def get_new_stupid_chess_game():
        return Game(
            type=GameType.STUPID_CHESS,
            placePieceRequired=True,
            possiblePiecesToBePlaced=GameFactory.STUPID_CHESS_INTIAL_PIECES_TO_BE_PLACED,
            squaresToBePlaced=GameFactory.STUPID_CHESS_INTIAL_SQUARES_TO_BE_PLACED,
            currentTurn=Color.BLACK,
            blackScore=1,
            whiteScore=1,
        )


GAME_TYPE_TO_CREATE_FUNCTION = {
    GameType.STUPID_CHESS: GameFactory.get_new_stupid_chess_game
}
