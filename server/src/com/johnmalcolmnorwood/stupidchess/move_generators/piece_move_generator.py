#!/usr/local/bin/python


class PieceMoveGenerator(object):
    def __init__(self, possible_move_game_state):
        self.__possible_move_game_state = possible_move_game_state

    def get_possible_moves(self):
        raise NotImplementedError('PieceMoveGenerator must be subclassed to be used')



