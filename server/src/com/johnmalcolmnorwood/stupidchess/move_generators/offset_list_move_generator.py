#!/usr/local/bin/python


class OffsetListMoveGenerator:
    def __init__(self, offsets):
        self.__offsets = offsets

    def get_possible_moves(self, possible_move_game_state):
        possible_moves_including_off_board = map(
            possible_move_game_state.get_move_to_square_offset,
            self.__offsets,
        )

        return filter(lambda move: move is not None, possible_moves_including_off_board)
