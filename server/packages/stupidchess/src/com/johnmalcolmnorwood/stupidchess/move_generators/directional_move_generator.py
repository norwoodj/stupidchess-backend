#!/usr/local/bin/python


class DirectionalMoveGenerator:
    def __init__(self, directions):
        self.__directions = directions

    def get_possible_moves(self, possible_move_game_state):
        possible_moves = []

        for d in self.__directions:
            step = 1
            new_square = possible_move_game_state.get_square_for_move_offset(d * step)
            move = possible_move_game_state.get_move_to_square(new_square)
            while move is not None:
                possible_moves.append(move)

                if move.captures is not None:
                    break

                step += 1
                new_square = possible_move_game_state.get_square_for_move_offset(d * step)
                move = possible_move_game_state.get_move_to_square(new_square)

        return possible_moves
