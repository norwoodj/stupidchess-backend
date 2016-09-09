#!/usr/local/bin/python
from com.johnmalcolmnorwood.stupidchess.move_generators.possible_move_game_state import PossibleMoveGameState


class PossibleMoveService(object):
    def __init__(self, board_squares_for_game_type, board_middle_section_for_game_type):
        self.__board_squares_for_game_type = board_squares_for_game_type
        self.__board_middle_section_for_game_type = board_middle_section_for_game_type

    def get_possible_moves_from_square(self, square, game):
        possible_move_game_state = PossibleMoveGameState(
            game,
            square,
            self.__board_squares_for_game_type,
            self.__board_middle_section_for_game_type,
        )

        if possible_move_game_state.is_game_over():
            return []

        if not possible_move_game_state.is_square_on_board(square):
            return []

        if not possible_move_game_state.is_piece_on_square(square):
            return []
