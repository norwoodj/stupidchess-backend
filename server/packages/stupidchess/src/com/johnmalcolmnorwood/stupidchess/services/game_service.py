#!/usr/bin/env python
from ..factories.game_factory import create_new_game
from ..utils.game_utils import LIST_GAME_DICT_FIELDS
from ..models.game import Game
from ..models.piece import Color
from ..utils.game_rules import is_in_board_setup_mode, is_players_turn

DEFAULT_OFFSET = 0
DEFAULT_LIMIT = 10


class GameService:
    def __init__(self, possible_move_service):
        self.__possible_move_service = possible_move_service

    @staticmethod
    def __remove_unprivileged_game_info(game, user_uuid):
        if is_in_board_setup_mode(game) and game.whitePlayerUuid != game.blackPlayerUuid:
            user_color = Color.BLACK if game.blackPlayerUuid == user_uuid else Color.WHITE
            game.possiblePiecesToBePlaced = [p for p in game.possiblePiecesToBePlaced if p.color == user_color]
            game.pieces = [p for p in game.pieces if p.color == user_color]

        return game

    @staticmethod
    def __get_game_active_criteria():
        return {
            "$and": [
                {"blackPlayerScore": {"$gt": 0}},
                {"whitePlayerScore": {"$gt": 0}}
            ],
        }

    @staticmethod
    def __get_game_over_criteria():
        return {
            "$or": [
                {"blackPlayerScore": {"$eq": 0}},
                {"whitePlayerScore": {"$eq": 0}}
            ],
        }

    @staticmethod
    def __get_game_for_user_and_game_uuid_criteria(user_uuid, game_uuid):
        return {
            "$and": [
                {"_id": game_uuid},
                {"$or": [{"blackPlayerUuid": user_uuid}, {"whitePlayerUuid": user_uuid}]}
            ],
        }

    @staticmethod
    def __apply_default_paging_and_ordering(queryset, offset, limit):
        queryset = queryset.order_by("-lastUpdateTimestamp")
        queryset = queryset.only(*LIST_GAME_DICT_FIELDS)
        return queryset[offset:offset+limit]

    @staticmethod
    def create_game(game_type, game_auth_type, other_player):
        game = create_new_game(game_type, game_auth_type, other_player)
        game.save()
        return game

    @staticmethod
    def update_game(game_id, updates):
        Game.objects(_id=game_id).update(**updates)

    @staticmethod
    def query_games_for_user(user_uuid, game_type=None, extra_criteria=[]):
        game_is_of_type = [{"type": game_type}] if game_type is not None else []
        user_is_in_game = {
            "$or": [
                {"blackPlayerUuid": user_uuid},
                {"whitePlayerUuid": user_uuid},
            ],
        }

        query = {"$and": [user_is_in_game, *extra_criteria, *game_is_of_type]}
        return Game.objects(__raw__=query)

    @staticmethod
    def query_games_for_users(user_one_uuid, user_two_uuid, game_type=None, extra_criteria=[]):
        game_is_of_type = [{"type": game_type}] if game_type is not None else []
        users_are_in_game = {
            "$or": [
                {"$and": [{"blackPlayerUuid": user_one_uuid}, {"whitePlayerUuid": user_two_uuid}]},
                {"$and": [{"whitePlayerUuid": user_one_uuid}, {"blackPlayerUuid": user_two_uuid}]},
            ],
        }

        query = {"$and": [users_are_in_game, *extra_criteria, *game_is_of_type]}
        return Game.objects(__raw__=query)

    @staticmethod
    def query_two_player_games_for_user(user_uuid, game_type=None, extra_criteria=[]):
        game_is_of_type = [{"type": game_type}] if game_type is not None else []
        user_is_in_game_and_two_player = {
            "$or": [
                {"$and": [{"blackPlayerUuid": user_uuid}, {"whitePlayerUuid": {"$ne": user_uuid}}]},
                {"$and": [{"whitePlayerUuid": user_uuid}, {"blackPlayerUuid": {"$ne": user_uuid}}]},
            ],
        }

        query = {"$and": [user_is_in_game_and_two_player, *extra_criteria, *game_is_of_type]}
        return Game.objects(__raw__=query)

    @staticmethod
    def query_completed_two_player_games_for_user(user_uuid, game_type=None):
        return GameService.query_two_player_games_for_user(
            user_uuid=user_uuid,
            game_type=game_type,
            extra_criteria=[GameService.__get_game_over_criteria()],
        )

    @staticmethod
    def query_game_for_user_and_game_uuid(user_uuid, game_uuid):
        return Game.objects(__raw__=GameService.__get_game_for_user_and_game_uuid_criteria(user_uuid, game_uuid))

    @staticmethod
    def get_games_for_user(user_uuid, game_type=None, offset=DEFAULT_OFFSET, limit=DEFAULT_LIMIT, extra_criteria=[]):
        queryset = GameService.query_games_for_user(user_uuid, game_type, extra_criteria)
        return GameService.__apply_default_paging_and_ordering(queryset, offset, limit)

    @staticmethod
    def count_games_for_user(user_uuid, game_type=None, extra_criteria=[]):
        return len(GameService.query_games_for_user(user_uuid, game_type, extra_criteria))

    @staticmethod
    def get_games_for_users(user_one_uuid, user_two_uuid, game_type=None, offset=DEFAULT_OFFSET, limit=DEFAULT_LIMIT, extra_criteria=[]):
        queryset = GameService.query_games_for_users(user_one_uuid, user_two_uuid, game_type, extra_criteria)
        return GameService.__apply_default_paging_and_ordering(queryset, offset, limit)

    @staticmethod
    def count_games_for_users(user_one_uuid, user_two_uuid, game_type=None, extra_criteria=[]):
        return len(GameService.query_games_for_users(user_one_uuid, user_two_uuid, game_type, extra_criteria))

    @staticmethod
    def get_active_games_for_user(user_uuid, game_type=None, offset=DEFAULT_OFFSET, limit=DEFAULT_LIMIT):
        return GameService.get_games_for_user(
            user_uuid=user_uuid,
            game_type=game_type,
            offset=offset,
            limit=limit,
            extra_criteria=[GameService.__get_game_active_criteria()],
        )

    @staticmethod
    def get_active_games_for_users(user_one_uuid, user_two_uuid, game_type=None, offset=DEFAULT_OFFSET, limit=DEFAULT_LIMIT):
        return GameService.get_games_for_users(
            user_one_uuid=user_one_uuid,
            user_two_uuid=user_two_uuid,
            game_type=game_type,
            offset=offset,
            limit=limit,
            extra_criteria=[GameService.__get_game_active_criteria()],
        )

    @staticmethod
    def count_active_games_for_user(user_uuid, game_type=None):
        return GameService.count_games_for_user(
            user_uuid=user_uuid,
            game_type=game_type,
            extra_criteria=[GameService.__get_game_active_criteria()],
        )

    @staticmethod
    def count_active_games_for_users(user_one_uuid, user_two_uuid, game_type=None):
        return GameService.count_games_for_users(
            user_one_uuid=user_one_uuid,
            user_two_uuid=user_two_uuid,
            game_type=game_type,
            extra_criteria=[GameService.__get_game_active_criteria()],
        )

    @staticmethod
    def get_completed_games_for_user(user_uuid, game_type=None, offset=DEFAULT_OFFSET, limit=DEFAULT_LIMIT):
        return GameService.get_games_for_user(
            user_uuid=user_uuid,
            game_type=game_type,
            offset=offset,
            limit=limit,
            extra_criteria=[GameService.__get_game_over_criteria()],
        )

    @staticmethod
    def get_completed_games_for_users(user_one_uuid, user_two_uuid, game_type=None, offset=DEFAULT_OFFSET, limit=DEFAULT_LIMIT):
        return GameService.get_games_for_users(
            user_one_uuid=user_one_uuid,
            user_two_uuid=user_two_uuid,
            game_type=game_type,
            offset=offset,
            limit=limit,
            extra_criteria=[GameService.__get_game_over_criteria()],
        )

    @staticmethod
    def count_completed_games_for_user(user_uuid, game_type=None):
        return GameService.count_games_for_user(
            user_uuid=user_uuid,
            game_type=game_type,
            extra_criteria=[GameService.__get_game_over_criteria()],
        )

    @staticmethod
    def count_completed_games_for_users(user_one_uuid, user_two_uuid, game_type=None):
        return GameService.count_games_for_users(
            user_one_uuid=user_one_uuid,
            user_two_uuid=user_two_uuid,
            game_type=game_type,
            extra_criteria=[GameService.__get_game_over_criteria()],
        )

    @staticmethod
    def get_game_for_user_and_game_uuid(user_uuid, game_uuid, only_fields=None):
        queryset = Game.objects.only(*only_fields) if only_fields is not None else Game.objects
        game = queryset.get_or_404(__raw__=GameService.__get_game_for_user_and_game_uuid_criteria(user_uuid, game_uuid))
        return GameService.__remove_unprivileged_game_info(game, user_uuid)

    def get_possible_moves(self, user_uuid, game_uuid, square):
        game = GameService.get_game_for_user_and_game_uuid(user_uuid, game_uuid)

        if not is_players_turn(game, user_uuid):
            return []

        return self.__possible_move_service.get_possible_moves_from_square(square, game)
