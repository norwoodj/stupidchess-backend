#!/usr/local/bin/python
from com.johnmalcolmnorwood.stupidchess.models.move import Move


class AbstractMoveUpdateService(object):
    def get_move_type(self):
        raise NotImplementedError()

    def get_game_for_move(self, move, game_uuid):
        raise NotImplementedError()

    def get_moves_to_apply(self, move, game):
        raise NotImplementedError()

    def write_move_objects(self, moves_to_apply):
        moves = [self.get_move_for_insert(m) for m in moves_to_apply]
        Move.objects.insert(moves)

    def apply_game_updates_for_moves(self, moves_to_apply, game):
        raise NotImplementedError()

    def get_move_for_insert(self, move):
        raise NotImplementedError()
