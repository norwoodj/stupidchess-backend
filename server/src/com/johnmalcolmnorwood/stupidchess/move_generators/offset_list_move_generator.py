#!/usr/local/bin/python
from com.johnmalcolmnorwood.stupidchess.move_generators.piece_move_generator import PieceMoveGenerator


class OffsetListMoveGenerator(PieceMoveGenerator):
    def __init__(self, possible_move_game_state, offsets):
        super().__init__(possible_move_game_state)
        self.__offsets = offsets

    def get_possible_moves(self):
        possible_moves_including_off_board = map(
            self.possible_move_game_state.get_move_to_square_offset,
            self.__offsets,
        )

        return filter(lambda move: move is not None, possible_moves_including_off_board)
