#!/usr/bin/env python


class RecordService:
    def __init__(self, game_service):
        self.__game_service = game_service

    def get_user_records(self, user_uuid, game_type=None):
        completed_games = self.__game_service.count_completed_games_for_user(user_uuid=user_uuid, game_type=game_type)
        wins = self.__game_service.count_winning_games_for_user(user_uuid=user_uuid, game_type=game_type)
        losses = completed_games - wins

        return {
            "completedGames": completed_games,
            "wins": wins,
            "losses": losses,
        }
