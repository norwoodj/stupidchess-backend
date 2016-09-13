#!/usr/local/bin/python


class DirectionalMoveGenerator:
    def __init__(self, directions):
        self.__directions = directions

    def get_possible_moves(self, possible_move_game_state):
        possible_moves = []

        for d in self.__directions:
            step = 1
            move = possible_move_game_state.get_move_to_square_offset(d * step)
            while move is not None:
                possible_moves.append(move)

                if move.captures is not None:
                    break

                step += 1
                move = possible_move_game_state.get_move_to_square_offset(d * step)

        return possible_moves
