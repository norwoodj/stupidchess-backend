#!/usr/local/bin/python
from com.johnmalcolmnorwood.stupidchess.models.move import Move, MoveType
from com.johnmalcolmnorwood.stupidchess.models.piece import Color, PieceType
from com.johnmalcolmnorwood.stupidchess.utils import get_game_scores


class PossibleMoveGameState:
    def __init__(
        self,
        game,
        square,
        board_square_set,
        board_middle_section,
        can_capture_own_pieces,
        check,
        can_checkers_move_twice_on_first_move
    ):
        self.__game = game
        self.__pieces_by_square = {piece.square: piece for piece in game.pieces}
        self.__piece_being_moved = self.__pieces_by_square.get(square)
        self.__board_square_set = board_square_set
        self.__middle_board_section = board_middle_section
        self.__can_capture_own_pieces = can_capture_own_pieces
        self.__check = check
        self.__can_checkers_move_twice_on_first_move = can_checkers_move_twice_on_first_move

    def get_last_move_index(self):
        return self.__game.lastMove

    def is_game_over(self):
        black_score, white_score = get_game_scores(self.__game)
        return black_score == 0 or white_score == 0

    def is_pieces_turn(self):
        return self.__game.currentTurn == self.__piece_being_moved.color

    def can_piece_move_twice(self):
        return not self.has_piece_moved() and (
            self.__piece_being_moved.type == PieceType.PAWN or
            (self.__piece_being_moved.type == PieceType.CHECKER and self.__can_checkers_move_twice_on_first_move)
        )

    def has_piece_moved(self):
        return self.__piece_being_moved.firstMove is not None

    def get_forward_direction(self):
        return -1 if self.__piece_being_moved.color == Color.BLACK else 1

    def get_square_for_move_offset(self, offset, starting_square=None):
        starting_square = starting_square or self.__piece_being_moved.square
        new_square = starting_square + self.get_forward_direction() * offset
        return new_square

    def get_current_square(self):
        return self.__piece_being_moved.square

    def is_piece_on_square(self, square):
        return square in self.__pieces_by_square

    def is_square_on_board(self, square):
        return square in self.__board_square_set

    def is_square_in_middle_board(self, square):
        return square in self.__middle_board_section

    def get_piece_on_square(self, square):
        return self.__pieces_by_square.get(square)

    def is_piece_in_middle_board(self):
        return self.is_square_in_middle_board(self.__piece_being_moved.square)

    def is_place_piece_required(self):
        return len(self.__game.squaresToBePlaced) > 0

    def can_capture_on_square(self, square):
        piece_on_square = self.get_piece_on_square(square)
        if piece_on_square is None:
            return False

        return self.__can_capture_own_pieces or piece_on_square.color != self.__piece_being_moved.color

    def get_move_to_square(self, new_square, additional_captures=None):
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
            piece=self.__piece_being_moved,
            captures=captures,
        )
