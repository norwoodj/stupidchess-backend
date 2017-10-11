#!/usr/bin/env python
from itertools import groupby
from mongoengine import NotUniqueError

from .. import LOGGER
from ..exceptions import ForbiddenMoveException, InvalidMoveException, DuplicateMoveException
from ..models.piece import Color
from ..utils.game_rules import is_in_board_setup_mode, is_players_turn


class MoveApplicationService:
    def __init__(self, game_service, move_service, move_update_services):
        self.__game_service = game_service
        self.__move_service = move_service
        self.__move_update_service_by_type = {ms.get_move_type(): ms for ms in move_update_services}

    @staticmethod
    def __is_player_authorized_to_perform_move(game, user_uuid, move):
        color = move.piece.color if move.piece is not None else MoveApplicationService.__color_for_move_move(game, move)
        move_player_uuid = game.blackPlayerUuid if color == Color.BLACK else game.whitePlayerUuid
        return move_player_uuid == user_uuid

    @staticmethod
    def __color_for_move_move(game, move):
        for p in game.pieces:
            if p.square == move.startSquare:
                return p.color

    def apply_move(self, game_uuid, user_uuid, move):
        """
        Applies a move to the game with the input uuid. Will first retrieve a query that will ensure the game, then will
        ensure that the move is legal. Then it writes a move object to the move collection, and finally applies the
        update to the game state. The order of these operations along with indexes on the move and game collections
        guarantees the thread safety of this update.

        :param user_uuid: The uuid of the user applying the move
        :param game_uuid: The uuid of the game to which the move is being applied
        :param move: The move being applied
        """
        game = self.__game_service.get_game_for_game_uuid_and_user(game_uuid, user_uuid)

        if not MoveApplicationService.__is_player_authorized_to_perform_move(game, user_uuid, move):
            raise ForbiddenMoveException(move)

        if not (is_in_board_setup_mode(game) or is_players_turn(game, user_uuid)):
            color = move.piece.color if move.piece is not None else MoveApplicationService.__color_for_move_move(game, move)
            raise InvalidMoveException(move, f"It is not {color}'s turn to move!")

        LOGGER.debug(f"Applying move to game {game.get_id()} at lastMove {game.lastMove}: {move}")
        move_update_service = self.__move_update_service_by_type[move.type]
        moves_to_apply = move_update_service.get_moves_to_apply(move, game, user_uuid)

        if len(moves_to_apply) > 1:
            LOGGER.debug(f"Will apply additional move(s) to game {game.get_id()}: {', '.join(str(m) for m in moves_to_apply[1:])}")

        # Write the move objects, since we have a unique index on the index field of the move, these moves will fail
        # if some other request has already written a move on top of this game state. If however, this succeeds, we
        # essentially have locked the current game state for us to apply new moves until we update the lastMove field
        # of the game document to be the value of the last move applied in this list
        for idx, move in enumerate(moves_to_apply, start=game.lastMove + 1):
            move.gameUuid = game.get_id()
            move.index = idx

        try:
            self.__move_service.insert_many(
                [self.__move_update_service_by_type[m.type].get_move_for_insert(m) for m in moves_to_apply]
            )
        except NotUniqueError:
            raise DuplicateMoveException(moves_to_apply)

        LOGGER.debug(f"Successfully saved move indexes {', '.join(str(m.index) for m in moves_to_apply)} for game {game.get_id()}")

        # If we've made it here, the move was legal, and we've written the move to the collection, essentially locking
        # the game state for us to make an update on it. Apply those updates now
        for move_type, moves_for_type in groupby(moves_to_apply, key=lambda m: m.type):
            moves_for_type = list(moves_for_type)
            LOGGER.debug(f"Applying game updates for move type {move_type} to game {game.get_id()} for moves {', '.join(str(m) for m in moves_for_type)}")
            self.__move_update_service_by_type[move_type].apply_game_updates_for_moves(moves_for_type, game)

        return moves_to_apply
