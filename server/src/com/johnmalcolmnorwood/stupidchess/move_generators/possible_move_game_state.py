#!/usr/local/bin/python
from com.johnmalcolmnorwood.stupidchess.models.move import Move, MoveType
from com.johnmalcolmnorwood.stupidchess.models.game import GameType


class PossibleMoveGameState:
    def __init__(
        self,
        game,
        square,
        board_square_set_by_game_type,
        middle_section_by_game_type
    ):
        self.__game = game
        self.__pieces_by_square = {piece.square: piece for piece in game.pieces}
        self.__piece_being_moved = self.__pieces_by_square.get(square)
        self.__board_square_set = board_square_set_by_game_type.get(game.type, set())
        self.__middle_board_section = middle_section_by_game_type.get(game.type, set())
        self.__can_capture_own_pieces = game.type == GameType.STUPID_CHESS
        self.__check = game.type == GameType.STUPID_CHESS

    def is_game_over(self):
        return self.__game.blackScore == 0 or self.__game.whiteScore == 0

    def is_pieces_turn(self):
        return self.__game.currentTurn == self.__piece_being_moved.color

    def is_piece_on_square(self, square):
        return square in self.__pieces_by_square

    def get_piece_on_square(self, square):
        return self.__pieces_by_square.get(square)

    def is_square_on_board(self, square):
        return square in self.__board_square_set

    def is_place_piece_required(self):
        return len(self.__game.squaresToBePlaced) > 0

    def can_capture_on_square(self, square):
        piece_on_square = self.get_piece_on_square(square)
        if piece_on_square is None:
            return False

        return self.__can_capture_own_pieces or piece_on_square.color != self.__piece_being_moved.color

    def get_move_to_square_offset(self, square_offset):
        new_square = self.__piece_being_moved.square + square_offset
        if not self.is_square_on_board(new_square):
            return None

        piece_on_square = self.get_piece_on_square(new_square)
        captures = [piece_on_square] if self.can_capture_on_square(new_square) else []
        move_object = Move(
            startSquare=self.__piece_being_moved.square,
            destinationSquare=new_square,
            type=MoveType.MOVE,
            piece=self.__piece_being_moved,
            captures=captures,

        )

        return {
            'move': Move(),
        }

