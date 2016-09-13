#!/usr/local/bin/python


class PawnLikeMoveGenerator:
    """
    This class generates moves for pawn-like pieces. That is, pieces that move one space in a direction if there is a
    vacant space there, but can also move two places on it's first move. This is going to be used for the checker in
    addition to the Pawn, because in Stupid Chess checkers can move twice on their first move because we thought that
    was a good idea for some reason
    """
    def __init__(self, directions, middle_board_forward_offset=None):
        self.__directions = directions
        self.__middle_board_forward_offset = middle_board_forward_offset

    def get_possible_moves(self, possible_move_game_state):
        moves = []
        for d in self.__directions:
            can_move_forward_once = PawnLikeMoveGenerator.add_non_capturing_move(
                moves,
                d,
                possible_move_game_state
            )

            # If the first step forward wasn't blocked and this piece hasn't moved yet, see if move forward two
            if can_move_forward_once and possible_move_game_state.can_piece_move_twice():
                self.add_non_capturing_move(moves, d * 2, possible_move_game_state)

        if self.__middle_board_forward_offset is not None and possible_move_game_state.is_piece_in_middle_board():
            self.add_non_capturing_move(
                moves,
                self.__middle_board_forward_offset,
                possible_move_game_state,
            )

        return moves

    @staticmethod
    def add_non_capturing_move(moves, square_offset, possible_move_game_state):
        true_offset = square_offset * possible_move_game_state.get_forward_direction()
        new_square = possible_move_game_state.get_current_square() + true_offset

        can_move = (
            possible_move_game_state.is_square_on_board(new_square) and
            not possible_move_game_state.is_piece_on_square(new_square)
        )

        if can_move:
            moves.append(possible_move_game_state.get_move_to_square_offset(true_offset))
            return True

        return False
