#!/usr/bin/env python
from itertools import groupby
from .. import LOGGER
from ..exceptions import ForbiddenMoveException, InvalidMoveException
from ..models.move import Move
from ..models.piece import Color
from ..utils.game_rules import is_in_board_setup_mode, is_players_turn

DEFAULT_OFFSET = 0
DEFAULT_LIMIT = 10


class MoveService:
    def __init__(self, move_dao, game_service):
        self.__game_service = game_service
        self.__move_dao = move_dao

    @staticmethod
    def __should_limit_moves_returned(game):
        return is_in_board_setup_mode(game) and game.whitePlayerUuid != game.blackPlayerUuid

    @staticmethod
    def __get_default_ordering():
        return ["-index"]

    @staticmethod
    def __get_moves_for_game_criteria(game_uuid):
        return {"gameUuid": game_uuid}

    @staticmethod
    def __get_moves_of_color_criteria(color):
        return {"piece.color": color}

    def __get_moves_for_game_and_user_criteria(self, game_uuid, user_uuid):
        game = self.__game_service.get_game_for_game_uuid_and_user(
            game_uuid=game_uuid,
            user_uuid=user_uuid,
            only_fields=["type", "lastMove", "blackPlayerUuid", "whitePlayerUuid"],
        )

        if not MoveService.__should_limit_moves_returned(game):
            return MoveService.__get_moves_for_game_criteria(game_uuid)

        color_moves_to_retrieve = Color.BLACK if game.blackPlayerUuid == user_uuid else Color.WHITE
        return {
            "$and": [
                MoveService.__get_moves_for_game_criteria(game_uuid),
                MoveService.__get_moves_of_color_criteria(color_moves_to_retrieve),
            ],
        }

    def insert_many(self, moves):
        return self.__move_dao.insert_many(moves)

    def get_moves_for_game_and_user(self, game_uuid, user_uuid, offset=DEFAULT_OFFSET, limit=DEFAULT_LIMIT):
        query = self.__get_moves_for_game_and_user_criteria(game_uuid, user_uuid)
        return self.__move_dao.find(
            query=query,
            offset=offset,
            limit=limit,
            order_by_fields=MoveService.__get_default_ordering(),
        )

    def count_moves_for_game_and_user(self, game_uuid, user_uuid):
        query = self.__get_moves_for_game_and_user_criteria(game_uuid, user_uuid)
        return self.__move_dao.count(query=query)
