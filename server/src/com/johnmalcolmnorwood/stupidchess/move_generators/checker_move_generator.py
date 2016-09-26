#!/usr/local/bin/python
from com.johnmalcolmnorwood.stupidchess.move_generators.forward_non_capturing_move_generator import (
    ForwardNonCapturingMoveGenerator,
)


class CheckerMoveGenerator:
    def __init__(self, forward_offsets, middle_board_offset=None):
        self.__forward_non_capturing_move_generator = ForwardNonCapturingMoveGenerator(
            forward_offsets,
            middle_board_offset
        )

        self.__possible_capture_moves = [
            (capture_offset, capture_offset * 2) for capture_offset in forward_offsets
        ]

        self.__middle_board_possible_capture_move = (middle_board_offset, middle_board_offset * 2) \
            if middle_board_offset is not None \
            else None

    def get_possible_moves(self, possible_move_game_state):
        moves = []
        self.__add_moves_from_square(moves, possible_move_game_state, possible_move_game_state.get_current_square())

        if possible_move_game_state.can_piece_move_twice():
            second_moves = []
            for m in moves:
                self.__add_moves_from_square(
                    second_moves,
                    possible_move_game_state,
                    m.destinationSquare,
                    m.captures,
                )

            moves += second_moves

        return moves

    def __add_moves_from_square(self, moves, possible_move_game_state, starting_square, captures_so_far=None):
        non_capturing_moves = self.__forward_non_capturing_move_generator.get_possible_moves(
            possible_move_game_state,
            starting_square,
        )

        for m in non_capturing_moves:
            m.captures = captures_so_far

        moves += non_capturing_moves

        captures_set = set() if captures_so_far is None else set(map(lambda c: c.square, captures_so_far))

        self.__add_captures_from_square(
            moves,
            possible_move_game_state,
            starting_square,
            captures_set,
        )

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
