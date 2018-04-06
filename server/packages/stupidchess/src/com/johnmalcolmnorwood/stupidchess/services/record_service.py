#!/usr/bin/env python
from ..models.game import GameResult, GameType


class RecordService:
    def __init__(self, game_service):
        self.__game_service = game_service

    @staticmethod
    def __get_game_result_projection(user_uuid):
        not_one_player = {
            "$not": {
                "$and": [
                    {"$eq": ["$blackPlayerUuid", user_uuid]},
                    {"$eq": ["$whitePlayerUuid", user_uuid]},
                ],
            },
        }

        return {
            "$project": {
                "type": 1,
                "blackPlayerUuid": 1,
                "whitePlayerUuid": 1,
                "blackPlayerScore": 1,
                "whitePlayerScore": 1,
                "gameResult": {
                    "$cond": {
                        "if": {
                            "$or": [
                                {"$and": [{"$eq": ["$blackPlayerUuid", user_uuid]}, {"$eq": ["$whitePlayerScore", 0]}]},
                                {"$and": [not_one_player, {"$eq": ["$whitePlayerUuid", user_uuid]}, {"$eq": ["$blackPlayerScore", 0]}]},

                            ],
                        },
                        "then": GameResult.WIN,
                        "else": GameResult.LOSS,
                    },
                },
            },
        }

    @staticmethod
    def __get_game_type_and_result_group():
        return {
            "$group": {
                "_id": {
                    "$concat": ["$type", ".", "$gameResult"],
                },
                "count": {"$sum": 1},
                "pointDifferential": {"$sum": {"$add": ["$blackPlayerScore", "$whitePlayerScore"]}},
            }
        }

    @staticmethod
    def __convert_to_per_game_type_records(results_for_game_type_and_result):
        records = {
            game_type: {
                "wins": 0,
                "losses": 0,
                "pointDifferential": 0,
            } for game_type in GameType.all()
        }

        for r in results_for_game_type_and_result:
            game_type, game_result = r["_id"].split(".")

            multiplier = -1 if game_result == GameResult.LOSS else 1
            result_key = "losses" if game_result == GameResult.LOSS else "wins"
            records[game_type]["pointDifferential"] += multiplier * r["pointDifferential"]
            records[game_type][result_key] = r["count"]

        return records

    def get_user_records(self, user_uuid, include_one_player_games):
        query_games_method = self.__game_service.query_completed_games_for_user \
            if include_one_player_games \
            else self.__game_service.query_completed_two_player_games_for_user

        results_for_game_type_and_result = query_games_method(
            user_uuid,
        ).aggregate(
            RecordService.__get_game_result_projection(user_uuid),
            RecordService.__get_game_type_and_result_group(),
        )

        return RecordService.__convert_to_per_game_type_records(results_for_game_type_and_result)
