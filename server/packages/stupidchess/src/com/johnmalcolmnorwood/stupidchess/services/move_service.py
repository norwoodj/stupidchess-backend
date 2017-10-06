#!/usr/bin/env python
from itertools import groupby
from .. import LOGGER
from ..exceptions import ForbiddenMoveException, InvalidMoveException
from ..models.game import GameType
from ..models.move import Move
from ..models.piece import Color
from ..utils.game_rules import is_in_board_setup_mode, is_players_turn

DEFAULT_OFFSET = 0
DEFAULT_LIMIT = 10


class MoveService:
    def __init__(self, move_update_services, game_service):
        self.__move_update_service_by_type = {ms.get_move_type(): ms for ms in move_update_services}
        self.__game_service = game_service

    @staticmethod
    def __color_for_move_move(game, move):
        for p in game.pieces:
            if p.square == move.startSquare:
                return p.color

    @staticmethod
    def __is_player_authorized_to_perform_move(game, user_uuid, move):
        color = move.piece.color if move.piece is not None else MoveService.__color_for_move_move(game, move)
        move_player_uuid = game.blackPlayerUuid if color == Color.BLACK else game.whitePlayerUuid
        return move_player_uuid == user_uuid

    @staticmethod
    def __should_limit_moves_returned(game):
        return game.type == GameType.STUPID_CHESS and game.lastMove < 23 and game.whitePlayerUuid != game.blackPlayerUuid

    @staticmethod
    def __apply_default_paging_and_ordering(queryset, offset, limit):
        queryset = queryset.order_by("-index")
        return queryset[offset:offset+limit]

    @staticmethod
    def query_moves_for_game(game_uuid, extra_criteria=[]):
        if len(extra_criteria) == 0:
            return Move.objects(gameUuid=game_uuid)

        move_criteria = {
            "$and": [
                {"gameUuid": game_uuid},
                *extra_criteria,
            ],
        }

        return Move.objects(__raw__=move_criteria)

    def get_moves_for_game_and_user(self, game_uuid, user_uuid, offset=DEFAULT_OFFSET, limit=DEFAULT_LIMIT):
        game = self.__game_service.get_game_for_user_and_game_uuid(
            user_uuid=user_uuid,
            game_uuid=game_uuid,
            only_fields=["type", "lastMove", "blackPlayerUuid", "whitePlayerUuid"],
        )

        if not MoveService.__should_limit_moves_returned(game):
            queryset = MoveService.query_moves_for_game(game_uuid)
            return MoveService.__apply_default_paging_and_ordering(queryset, offset, limit)

        color_moves_to_retrieve = Color.BLACK if game.blackPlayerUuid == user_uuid else Color.WHITE
        queryset = MoveService.query_moves_for_game(game_uuid, extra_criteria=[{"piece.color": color_moves_to_retrieve}])
        return MoveService.__apply_default_paging_and_ordering(queryset, offset, limit)

    def apply_move(self, user_uuid, game_uuid, move):
        """
        Applies a move to the game with the input uuid. Will first retrieve a query that will ensure the game, then will
        ensure that the move is legal. Then it writes a move object to the move collection, and finally applies the
        update to the game state. The order of these operations along with indexes on the move and game collections
        guarantees the thread safety of this update.

        :param user_uuid: The uuid of the user applying the move
        :param game_uuid: The uuid of the game to which the move is being applied
        :param move: The move being applied
        """
        game = self.__game_service.get_game_for_user_and_game_uuid(user_uuid, game_uuid)

        if not MoveService.__is_player_authorized_to_perform_move(game, user_uuid, move):
            raise ForbiddenMoveException(move)

        if not (is_in_board_setup_mode(game) or is_players_turn(game, user_uuid)):
            color = move.piece.color if move.piece is not None else MoveService.__color_for_move_move(game, move)
            raise InvalidMoveException(move, f"It is not {color}'s turn to move!")

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
