#!/usr/local/bin/python
from com.johnmalcolmnorwood.stupidchess.move_generators.piece_move_generator import PieceMoveGenerator


class KingMoveGenerator(PieceMoveGenerator):
    DIRECTIONS = (-10, -9, 1, 11, 10, 9, -1, -11)

    def get_possible_moves(self):
        possible_moves_including_off_board = map(
            self.possible_move_game_state.get_move_to_square_offset,
            KingMoveGenerator.DIRECTIONS,
        )

        return filter(lambda move: move is not None, possible_moves_including_off_board)
