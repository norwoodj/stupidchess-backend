#!/usr/local/bin/python
from ..models.game import GameType
from ..move_generators.possible_move_game_state import PossibleMoveGameState
from ..factories.piece_move_generator_factory import get_piece_move_generator_for_piece
from ..utils.game_rules import is_in_board_setup_mode, is_players_turn


class PossibleMoveService:
    def __init__(self, game_service, board_squares_for_game_type, board_middle_section_for_game_type):
        self.__game_service = game_service
        self.__board_squares_for_game_type = board_squares_for_game_type
        self.__board_middle_section_for_game_type = board_middle_section_for_game_type

    def get_possible_moves_from_square(
        self,
        square,
        game=None,
        game_uuid=None,
        user_uuid=None,
    ):
        game = game or self.__game_service.get_game_for_user_and_game_uuid(user_uuid, game_uuid)

        if not is_players_turn(game, user_uuid) or is_in_board_setup_mode(game):
            return []

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
