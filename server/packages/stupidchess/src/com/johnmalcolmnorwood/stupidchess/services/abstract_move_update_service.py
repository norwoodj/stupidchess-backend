#!/usr/local/bin/python


class AbstractMoveUpdateService:
    def get_move_type(self):
        raise NotImplementedError()

    def get_moves_to_apply(self, move, game, user_uuid):
        raise NotImplementedError()

    def apply_game_updates_for_moves(self, moves_to_apply, game):
        raise NotImplementedError()

    def get_move_for_insert(self, move):
        raise NotImplementedError()
