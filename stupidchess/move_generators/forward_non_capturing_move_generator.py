#!/usr/local/bin/python


class ForwardNonCapturingMoveGenerator:
    """
    This class generates moves for forward moving non capturing pieces. That is, pieces that move one space in a
    direction if there is a vacant space there. These pieces also gain an additional direction of movement in the middle
    board in Stupid Chess. This is going to be used for the checker in addition to the Pawn, because in Stupid Chess
    checkers can move twice on their first move because we thought that was a good idea for some reason
    """

    def __init__(self, directions, middle_board_forward_offset=None):
        self.__directions = directions
        self.__middle_board_forward_offset = middle_board_forward_offset

    def get_possible_moves(self, possible_move_game_state, starting_square=None):
        moves = []
        starting_square = (
            starting_square or possible_move_game_state.get_current_square()
        )

        for d in self.__directions:
            ForwardNonCapturingMoveGenerator.add_non_capturing_move(
                moves,
                starting_square,
                d,
                possible_move_game_state,
            )

        if (
            self.__middle_board_forward_offset is not None
            and possible_move_game_state.is_piece_in_middle_board()
        ):
            self.add_non_capturing_move(
                moves,
                starting_square,
                self.__middle_board_forward_offset,
                possible_move_game_state,
            )

        return moves

    @staticmethod
    def add_non_capturing_move(
        moves, starting_square, square_offset, possible_move_game_state
    ):
        new_square = possible_move_game_state.get_square_for_move_offset(
            square_offset, starting_square
        )

        can_move = possible_move_game_state.is_square_on_board(
            new_square
        ) and not possible_move_game_state.is_piece_on_square(new_square)

        if can_move:
            moves.append(possible_move_game_state.get_move_to_square(new_square))
