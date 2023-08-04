#!/usr/bin/env python
from ..factories.game_factory import create_new_game
from ..utils.game_utils import LIST_GAME_DICT_FIELDS
from ..models.piece import Color
from ..utils.game_rules import is_in_board_setup_mode, is_square_in_setup_zone_for_color

DEFAULT_OFFSET = 0
DEFAULT_LIMIT = 10


class GameService:
    def __init__(self, game_dao):
        self.__game_dao = game_dao

    @staticmethod
    def __remove_unprivileged_game_info(game, user_uuid):
        if (
            is_in_board_setup_mode(game)
            and game.whitePlayerUuid != game.blackPlayerUuid
        ):
            user_color = (
                Color.BLACK if game.blackPlayerUuid == user_uuid else Color.WHITE
            )
            game.possiblePiecesToBePlaced = [
                p for p in game.possiblePiecesToBePlaced if p.color == user_color
            ]
            game.pieces = [p for p in game.pieces if p.color == user_color]
            game.squaresToBePlaced = [
                s
                for s in game.squaresToBePlaced
                if is_square_in_setup_zone_for_color(user_color, s)
            ]

        return game

    @staticmethod
    def __add_game_type_criteria(query, game_type=None):
        if game_type is None:
            return query

        return {"$and": [query, {"type": game_type}]}

    @staticmethod
    def __get_game_active_criteria():
        return {
            "$and": [
                {"blackPlayerScore": {"$gt": 0}},
                {"whitePlayerScore": {"$gt": 0}},
            ],
        }

    @staticmethod
    def __get_game_completed_criteria():
        return {
            "$or": [{"blackPlayerScore": {"$eq": 0}}, {"whitePlayerScore": {"$eq": 0}}],
        }

    @staticmethod
    def __get_games_for_user_criteria(user_uuid):
        return {
            "$or": [
                {"blackPlayerUuid": user_uuid},
                {"whitePlayerUuid": user_uuid},
            ],
        }

    @staticmethod
    def __get_game_for_user_and_game_uuid_criteria(user_uuid, game_uuid):
        return {
            "$and": [
                {"_id": game_uuid},
                GameService.__get_games_for_user_criteria(user_uuid),
            ],
        }

    @staticmethod
    def __get_games_for_users_criteria(user_one_uuid, user_two_uuid):
        return {
            "$or": [
                {
                    "$and": [
                        {"blackPlayerUuid": user_one_uuid},
                        {"whitePlayerUuid": user_two_uuid},
                    ]
                },
                {
                    "$and": [
                        {"whitePlayerUuid": user_one_uuid},
                        {"blackPlayerUuid": user_two_uuid},
                    ]
                },
            ],
        }

    @staticmethod
    def __get_two_player_games_for_user_criteria(user_uuid):
        return {
            "$or": [
                {
                    "$and": [
                        {"blackPlayerUuid": user_uuid},
                        {"whitePlayerUuid": {"$ne": user_uuid}},
                    ]
                },
                {
                    "$and": [
                        {"whitePlayerUuid": user_uuid},
                        {"blackPlayerUuid": {"$ne": user_uuid}},
                    ]
                },
            ],
        }

    @staticmethod
    def __get_specific_games_for_user_criteria(
        user_uuid, game_type=None, extra_criteria=[]
    ):
        query = {
            "$and": [
                GameService.__get_games_for_user_criteria(user_uuid),
                *extra_criteria,
            ]
        }

        return GameService.__add_game_type_criteria(query, game_type)

    @staticmethod
    def __get_specific_games_for_users_criteria(
        user_one_uuid, user_two_uuid, game_type=None, extra_criteria=[]
    ):
        query = {
            "$and": [
                GameService.__get_games_for_users_criteria(
                    user_one_uuid, user_two_uuid
                ),
                *extra_criteria,
            ]
        }

        return GameService.__add_game_type_criteria(query, game_type)

    @staticmethod
    def __get_list_game_only_fields():
        return LIST_GAME_DICT_FIELDS

    @staticmethod
    def __get_default_ordering():
        return ["-lastUpdateTimestamp"]

    def create_game(self, game_type, game_auth_type, other_player):
        game = create_new_game(game_type, game_auth_type, other_player)
        return self.__game_dao.insert(game)

    def update_game(self, game_uuid, updates):
        return self.__game_dao.update(game_uuid, updates)

    def game_with_uuid_for_user_exists(self, game_uuid, user_uuid):
        return (
            self.__game_dao.count(
                GameService.__get_game_for_user_and_game_uuid_criteria(
                    user_uuid, game_uuid
                )
            )
            > 0
        )

    def get_game_for_game_uuid_and_user(self, game_uuid, user_uuid, only_fields=None):
        query = GameService.__get_game_for_user_and_game_uuid_criteria(
            user_uuid, game_uuid
        )
        game = self.__game_dao.find_one(query, only_fields)
        return GameService.__remove_unprivileged_game_info(game, user_uuid)

    def get_active_games_for_user(
        self,
        user_uuid,
        game_type=None,
        offset=DEFAULT_OFFSET,
        limit=DEFAULT_LIMIT,
    ):
        query = GameService.__get_specific_games_for_user_criteria(
            user_uuid=user_uuid,
            game_type=game_type,
            extra_criteria=[GameService.__get_game_active_criteria()],
        )

        return self.__game_dao.find(
            query=query,
            offset=offset,
            limit=limit,
            only_fields=GameService.__get_list_game_only_fields(),
            order_by_fields=GameService.__get_default_ordering(),
        )

    def get_active_games_for_users(
        self,
        user_one_uuid,
        user_two_uuid,
        game_type=None,
        offset=DEFAULT_OFFSET,
        limit=DEFAULT_LIMIT,
    ):
        query = GameService.__get_specific_games_for_users_criteria(
            user_one_uuid=user_one_uuid,
            user_two_uuid=user_two_uuid,
            game_type=game_type,
            extra_criteria=[GameService.__get_game_active_criteria()],
        )

        return self.__game_dao.find(
            query=query,
            offset=offset,
            limit=limit,
            only_fields=GameService.__get_list_game_only_fields(),
            order_by_fields=GameService.__get_default_ordering(),
        )

    def count_active_games_for_user(self, user_uuid, game_type=None):
        query = GameService.__get_specific_games_for_user_criteria(
            user_uuid=user_uuid,
            game_type=game_type,
            extra_criteria=[GameService.__get_game_active_criteria()],
        )

        return self.__game_dao.count(query)

    def count_active_games_for_users(
        self, user_one_uuid, user_two_uuid, game_type=None
    ):
        query = GameService.__get_specific_games_for_users_criteria(
            user_one_uuid=user_one_uuid,
            user_two_uuid=user_two_uuid,
            game_type=game_type,
            extra_criteria=[GameService.__get_game_active_criteria()],
        )

        return self.__game_dao.count(query)

    def get_completed_games_for_user(
        self,
        user_uuid,
        game_type=None,
        offset=DEFAULT_OFFSET,
        limit=DEFAULT_LIMIT,
    ):
        query = GameService.__get_specific_games_for_user_criteria(
            user_uuid=user_uuid,
            game_type=game_type,
            extra_criteria=[GameService.__get_game_completed_criteria()],
        )

        return self.__game_dao.find(
            query=query,
            offset=offset,
            limit=limit,
            only_fields=GameService.__get_list_game_only_fields(),
            order_by_fields=GameService.__get_default_ordering(),
        )

    def get_completed_games_for_users(
        self,
        user_one_uuid,
        user_two_uuid,
        game_type=None,
        offset=DEFAULT_OFFSET,
        limit=DEFAULT_LIMIT,
    ):
        query = GameService.__get_specific_games_for_users_criteria(
            user_one_uuid=user_one_uuid,
            user_two_uuid=user_two_uuid,
            game_type=game_type,
            extra_criteria=[GameService.__get_game_completed_criteria()],
        )

        return self.__game_dao.find(
            query=query,
            offset=offset,
            limit=limit,
            only_fields=GameService.__get_list_game_only_fields(),
            order_by_fields=GameService.__get_default_ordering(),
        )

    def count_completed_games_for_user(self, user_uuid, game_type=None):
        query = GameService.__get_specific_games_for_user_criteria(
            user_uuid=user_uuid,
            game_type=game_type,
            extra_criteria=[GameService.__get_game_completed_criteria()],
        )

        return self.__game_dao.count(query)

    def count_completed_games_for_users(
        self, user_one_uuid, user_two_uuid, game_type=None
    ):
        query = GameService.__get_specific_games_for_users_criteria(
            user_one_uuid=user_one_uuid,
            user_two_uuid=user_two_uuid,
            game_type=game_type,
            extra_criteria=[GameService.__get_game_completed_criteria()],
        )

        return self.__game_dao.count(query)

    def query_completed_games_for_user(self, user_uuid):
        query = {
            "$and": [
                GameService.__get_games_for_user_criteria(user_uuid),
                GameService.__get_game_completed_criteria(),
            ],
        }

        return self.__game_dao.query(query)

    def query_completed_two_player_games_for_user(self, user_uuid):
        query = {
            "$and": [
                GameService.__get_two_player_games_for_user_criteria(user_uuid),
                GameService.__get_game_completed_criteria(),
            ],
        }

        return self.__game_dao.query(query)
