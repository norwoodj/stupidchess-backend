#!/usr/local/bin/python
from com.johnmalcolmnorwood.stupidchess.move_generators.pawn_like_move_generator import PawnLikeMoveGenerator
from com.johnmalcolmnorwood.stupidchess.move_generators.move_generator_utils import Offsets


class CheckerMoveGenerator:
    def __init__(self, forward_offsets, middle_board_offset=None):
        self.__pawn_like_move_generator = PawnLikeMoveGenerator([9, 11], -9)
        self.__possible_capture_moves = [
            (capture_offset, capture_offset * 2) for capture_offset in forward_offsets
        ]

        self.__middle_board_possible_capture_move = (middle_board_offset, middle_board_offset * 2) \
            if middle_board_offset is not None \
            else None

    def get_possible_moves(self, possible_move_game_state):
        moves = self.__pawn_like_move_generator.get_possible_moves(possible_move_game_state)
        self.__add_captures_from_square(
            moves,
            possible_move_game_state,
            possible_move_game_state.get_current_square(),
            set(),
        )

        return moves

    @staticmethod
    def __can_capture_on_square(capture_square, move_square, possible_move_game_state):
        return (
            possible_move_game_state.is_square_on_board(capture_square) and
            possible_move_game_state.is_square_on_board(move_square) and
            possible_move_game_state.can_capture_on_square(capture_square) and
            not possible_move_game_state.is_piece_on_square(move_square)
        )

    def __add_capture_for_capture_move_pair(
        self,
        moves,
        possible_move_game_state,
        square,
        captured_squares,
        capture_offset,
        move_offset,
    ):
        capture_square = square + (capture_offset * possible_move_game_state.get_forward_direction())
        move_square = square + (move_offset * possible_move_game_state.get_forward_direction())
        print('Trying to Capture: {} in {}?'.format(capture_square, captured_squares))
        can_jump = (
            capture_square not in captured_squares and
            CheckerMoveGenerator.__can_capture_on_square(capture_square, move_square, possible_move_game_state)
        )

        if can_jump:
            branch_captured_squares = {capture_square, *captured_squares}
            captures = map(possible_move_game_state.get_piece_on_square, branch_captured_squares)

            move = possible_move_game_state.get_move_to_square(move_square, additional_captures=captures)
            moves.append(move)
            self.__add_captures_from_square(
                    moves,
                    possible_move_game_state,
                    move_square,
                    branch_captured_squares,
            )

    def __add_captures_from_square(
        self,
        moves,
        possible_move_game_state,
        square,
        captured_squares,
    ):
        for capture_offset, move_offset in self.__possible_capture_moves:
            self.__add_capture_for_capture_move_pair(
                moves,
                possible_move_game_state,
                square,
                captured_squares,
                capture_offset,
                move_offset,
            )

        if self.__middle_board_possible_capture_move is not None:
            capture_offset, move_offset = self.__middle_board_possible_capture_move

            self.__add_capture_for_capture_move_pair(
                    moves,
                    possible_move_game_state,
                    square,
                    captured_squares,
                    capture_offset,
                    move_offset,
            )
