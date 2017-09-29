#!/usr/bin/env python
from ..factories.game_factory import create_new_game
from ..models.game import Game
from ..models.piece import Color


class GameService:
    def __init__(self, possible_move_service):
        self.__possible_move_service = possible_move_service

    @staticmethod
    def __is_in_board_setup_mode(game):
        return game.type == "STUPID_CHESS" and game.lastMove < 23

    @staticmethod
    def __is_players_turn(game, user_uuid):
        return any([
            game.blackPlayerUuid == game.whitePlayerUuid,
            game.currentTurn == Color.BLACK and game.blackPlayerUuid == user_uuid,
            game.currentTurn == Color.WHITE and game.whitePlayerUuid == user_uuid,
        ])

    @staticmethod
    def __remove_unprivileged_moves(game, user_uuid):
        if GameService.__is_in_board_setup_mode(game) and game.whitePlayerUuid != game.blackPlayerUuid:
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
    def create_game(game_type, game_auth_type, other_player):
        game = create_new_game(game_type, game_auth_type, other_player)
        game.save()
        return game

    @staticmethod
    def update_game(game_id, updates):
        Game.objects(_id=game_id).update(**updates)

    @staticmethod
    def get_games_for_user(user_uuid, game_type=None, skip=0, results=10, extra_criteria=[]):
        games = GameService.query_games_for_user(user_uuid, game_type, extra_criteria)
        ordered = games.order_by("-lastUpdateTimestamp")
        game_page = ordered[skip:skip+results]

        return [GameService.__remove_unprivileged_moves(g, user_uuid) for g in game_page]

    @staticmethod
    def get_game_for_user_and_game_uuid(user_uuid, game_uuid):
        game = Game.objects.get_or_404(__raw__={
            "$and": [
                {"_id": game_uuid},
                {"$or": [{"blackPlayerUuid": user_uuid}, {"whitePlayerUuid": user_uuid}]}
            ],
        })

        return GameService.__remove_unprivileged_moves(game, user_uuid)

    @staticmethod
    def get_active_games_for_user(user_uuid, game_type=None, skip=0, results=10):
        return GameService.get_games_for_user(
            user_uuid=user_uuid,
            game_type=game_type,
            skip=skip,
            results=results,
            extra_criteria=[GameService.__get_game_active_criteria()],
        )

    @staticmethod
    def query_completed_two_player_games_for_user(user_uuid, game_type=None):
        return GameService.query_two_player_games_for_user(
            user_uuid=user_uuid,
            game_type=game_type,
            extra_criteria=[GameService.__get_game_over_criteria()],
        )

    @staticmethod
    def get_completed_games_for_user(user_uuid, game_type=None, skip=0, results=10):
        return GameService.get_games_for_user(
            user_uuid=user_uuid,
            game_type=game_type,
            skip=skip,
            results=results,
            extra_criteria=[GameService.__get_game_over_criteria()],
        )

    def get_possible_moves(self, user_uuid, game_uuid, square):
        game = GameService.get_game_for_user_and_game_uuid(user_uuid, game_uuid)

        if not GameService.__is_players_turn(game, user_uuid):
            return []

        return self.__possible_move_service.get_possible_moves_from_square(square, game)
