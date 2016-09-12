#!/usr/local/bin/python
from com.johnmalcolmnorwood.stupidchess.models.move import Move, MoveType
from com.johnmalcolmnorwood.stupidchess.models.game import GameType
from com.johnmalcolmnorwood.stupidchess.models.piece import Color
from com.johnmalcolmnorwood.stupidchess.utils import get_piece_for_move_db_object


class PossibleMoveGameState:
    def __init__(
        self,
        game,
        square,
        board_square_set,
        board_middle_section
    ):
        self.__game = game
        self.__pieces_by_square = {piece.square: piece for piece in game.pieces}
        self.__piece_being_moved = self.__pieces_by_square.get(square)
        self.__board_square_set = board_square_set
        self.__middle_board_section = board_middle_section
        self.__can_capture_own_pieces = game.type == GameType.STUPID_CHESS
        self.__check = game.type == GameType.STUPID_CHESS

    def get_last_move_index(self):
        return self.__game.lastMove

    def is_game_over(self):
        return self.__game.blackScore == 0 or self.__game.whiteScore == 0

    def is_pieces_turn(self):
        return self.__game.currentTurn == self.__piece_being_moved.color

    def has_piece_moved(self):
        return self.__piece_being_moved.firstMove is not None

    def get_forward_direction(self):
        return 1 if self.__piece_being_moved.color == Color.BLACK else -1

    def get_current_square(self):
        return self.__piece_being_moved.square

    def is_piece_on_square(self, square):
        return square in self.__pieces_by_square

    def get_piece_on_square(self, square):
        return self.__pieces_by_square.get(square)

    def is_square_in_middle_board(self, square):
        return square in self.__middle_board_section

    def is_square_on_board(self, square):
        return square in self.__board_square_set

    def is_place_piece_required(self):
        return len(self.__game.squaresToBePlaced) > 0

    def can_capture_on_square(self, square):
        piece_on_square = self.get_piece_on_square(square)
        if piece_on_square is None:
            return False

        return self.__can_capture_own_pieces or piece_on_square.color != self.__piece_being_moved.color

    def get_move_to_square_offset(self, square_offset, additional_captures=None):
        new_square = self.__piece_being_moved.square + square_offset
        if not self.is_square_on_board(new_square):
            return None

        if self.is_piece_on_square(new_square) and not self.can_capture_on_square(new_square):
            return None

        piece_on_square = self.get_piece_on_square(new_square)
        if piece_on_square is not None:
            captures = [piece_on_square, *additional_captures] if additional_captures is not None else [piece_on_square]
        else:
            captures = additional_captures

        return Move(
            startSquare=self.__piece_being_moved.square,
            destinationSquare=new_square,
            type=MoveType.MOVE,
            piece=get_piece_for_move_db_object(self.__piece_being_moved),
            captures=captures,
        )

