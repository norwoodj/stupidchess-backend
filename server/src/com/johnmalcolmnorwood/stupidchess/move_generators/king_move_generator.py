#!/usr/local/bin/python
from com.johnmalcolmnorwood.stupidchess.move_generators.piece_move_generator import PieceMoveGenerator


class KingMoveGenerator(PieceMoveGenerator):
    DIRECTIONS = (-10, -9, 1, 11, 10, 9, -1, -11)

    def get_possible_moves(self):
        for d in KingMoveGenerator.DIRECTIONS:
            if self.__possible_move_game_state:
                return []




