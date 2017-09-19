#!/usr/local/bin/python


class MoveApplicationService(object):
    def __init__(self, move_update_services):
        self.__move_update_service_by_type = {ms.get_move_type(): ms for ms in move_update_services}

    def apply_move(self, move, game_uuid):
        """
        Applies a move to the game with the input uuid. Will first retrieve a query that will ensure the game, then will
        ensure that the move is legal. Then it writes a move object to the move collection, and finally applies the
        update to the game state. The order of these operations along with indexes on the move and game collections
        guarantees the thread safety of this update.

        :param move: The move being applied
        :param game_uuid: The uuid of the game that the move is being applied to
        """
        move_update_service = self.__move_update_service_by_type[move.type]

        # Retrieve the current game, we will need it to check the legality of the move being performed, and to get the
        # index of the last move
        game = move_update_service.get_game_for_move(move, game_uuid)

        moves_to_apply = move_update_service.get_moves_to_apply(move, game)

        # Write the move objects, since we have a unique index on the index field of the move, these moves will fail
        # if some other request has already written a move on top of this game state. If however, this succeeds, we
        # essentially have locked the current game state for us to apply new moves until we update the lastMove field
        # of the game document to be the value of the last move applied in this list
        for idx, move in enumerate(moves_to_apply, start=game.lastMove + 1):
            move.gameUuid = game_uuid
            move.index = idx

        move_update_service.write_move_objects(moves_to_apply)

        # If we've made it here, the move was legal, and we've written the move to the collection, essentially locking
        # the game state for us to make an update on it. Apply those updates now
        move_update_service.apply_game_updates_for_moves(moves_to_apply, game)
        return moves_to_apply
