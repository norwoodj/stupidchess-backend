#!/usr/local/bin/python
from com.johnmalcolmnorwood.stupidchess.models.game import Game, GameType
from com.johnmalcolmnorwood.stupidchess.move_generators.possible_move_game_state import PossibleMoveGameState
from com.johnmalcolmnorwood.stupidchess.factories.piece_move_generator_factory import get_piece_move_generator_for_piece


class PossibleMoveService(object):
    def __init__(self, board_squares_for_game_type, board_middle_section_for_game_type):
        self.__board_squares_for_game_type = board_squares_for_game_type
        self.__board_middle_section_for_game_type = board_middle_section_for_game_type

    def get_possible_moves_from_square(self, square, game):
        board_square_set = self.__board_squares_for_game_type.get(game.type, set())
        board_middle_square_set = self.__board_middle_section_for_game_type.get(game.type, set())
        can_capture_own_pieces = game.type == GameType.STUPID_CHESS
        check = game.type == GameType.CHESS
        can_checkers_move_twice_on_first_move = game.type == GameType.STUPID_CHESS

        possible_move_game_state = PossibleMoveGameState(
            game,
            square,
            board_square_set=board_square_set,
            board_middle_section=board_middle_square_set,
            can_capture_own_pieces=can_capture_own_pieces,
            check=check,
            can_checkers_move_twice_on_first_move=can_checkers_move_twice_on_first_move,
        )

        if possible_move_game_state.is_game_over():
            return []

        if not possible_move_game_state.is_square_on_board(square):
            return []

        if not possible_move_game_state.is_piece_on_square(square):
            return []

        if not possible_move_game_state.is_pieces_turn():
            return []

        piece = possible_move_game_state.get_piece_on_square(square)
        piece_move_generator = get_piece_move_generator_for_piece(piece.type)

        return piece_move_generator.get_possible_moves(possible_move_game_state)
