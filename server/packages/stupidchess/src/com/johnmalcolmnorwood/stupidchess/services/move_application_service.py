#!/usr/local/bin/python
from itertools import groupby
from .. import LOGGER
from ..models.move import Move


class MoveApplicationService:
    def __init__(self, move_update_services):
        self.__move_update_service_by_type = {ms.get_move_type(): ms for ms in move_update_services}

    def apply_move(self, game, move):
        """
        Applies a move to the game with the input uuid. Will first retrieve a query that will ensure the game, then will
        ensure that the move is legal. Then it writes a move object to the move collection, and finally applies the
        update to the game state. The order of these operations along with indexes on the move and game collections
        guarantees the thread safety of this update.

        :param game: The game that the move is being applied to
        :param move: The move being applied
        """
        LOGGER.debug(f"Applying move to game {game.get_id()} at lastMove {game.lastMove}: {move}")
        move_update_service = self.__move_update_service_by_type[move.type]
        moves_to_apply = move_update_service.get_moves_to_apply(move, game)

        if len(moves_to_apply) > 1:
            LOGGER.debug(f"Will apply additional move(s) to game {game.get_id()}: {', '.join(str(m) for m in moves_to_apply[1:])}")

        # Write the move objects, since we have a unique index on the index field of the move, these moves will fail
        # if some other request has already written a move on top of this game state. If however, this succeeds, we
        # essentially have locked the current game state for us to apply new moves until we update the lastMove field
        # of the game document to be the value of the last move applied in this list
        for idx, move in enumerate(moves_to_apply, start=game.lastMove + 1):
            move.gameUuid = game.get_id()
            move.index = idx

        Move.objects.insert([self.__move_update_service_by_type[m.type].get_move_for_insert(m) for m in moves_to_apply])
        LOGGER.debug(f"Successfully saved move indexes {', '.join(str(m.index) for m in moves_to_apply)} for game {game.get_id()}")

        # If we've made it here, the move was legal, and we've written the move to the collection, essentially locking
        # the game state for us to make an update on it. Apply those updates now
        for move_type, moves_for_type in groupby(moves_to_apply, key=lambda m: m.type):
            moves_for_type = list(moves_for_type)
            LOGGER.debug(f"Applying game updates for move type {move_type} to game {game.get_id()} for moves {', '.join(str(m) for m in moves_for_type)}")
            self.__move_update_service_by_type[move_type].apply_game_updates_for_moves(moves_for_type, game)

        return moves_to_apply
