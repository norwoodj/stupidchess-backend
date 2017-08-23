#!/usr/local/bin/python


class OffsetListMoveGenerator:
    def __init__(self, offsets):
        self.__offsets = offsets

    def get_possible_moves(self, possible_move_game_state):
        new_squares = map(possible_move_game_state.get_square_for_move_offset, self.__offsets)
        possible_moves_including_off_board = map(possible_move_game_state.get_move_to_square, new_squares)
        return list(filter(lambda move: move is not None, possible_moves_including_off_board))
