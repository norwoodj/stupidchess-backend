#!/usr/local/bin/python
from com.johnmalcolmnorwood.stupidchess.move_generators.piece_move_generator import PieceMoveGenerator


class DirectionalMoveGenerator(PieceMoveGenerator):
    def __init__(self, possible_move_game_state, directions):
        super().__init__(possible_move_game_state)
        self.__directions = directions

    def get_possible_moves(self):
        possible_moves = []

        for d in self.__directions:
            step = 1
            move = self.possible_move_game_state.get_move_to_square_offset(d * step)
            while move is not None:
                possible_moves.append(move)

                if len(move.captures) > 0:
                    break

                step += 1
                move = self.possible_move_game_state.get_move_to_square_offset(d * step)


        return possible_moves
