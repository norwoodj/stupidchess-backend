from ..models.game import Game


class RecordService:
    @staticmethod
    def get_user_records(user_uuid):
        is_current_user_in_game = {"$or": [{"blackPlayerUuid": user_uuid}, {"whitePlayerUuid": user_uuid}]}
        is_two_player_game = {"blackPlayerUuid": {"$ne":  "whitePlayerUuid"}}
        is_game_over = {"$or": [{"blackPlayerScore": 0}, {"whitePlayerScore": 0}]}
        group_by = {
            "_id": {
                "$cond": {
                    "if": {"$eq": ["$blackPlayerUuid", user_uuid]},
                    "then": {
                        "$cond": {
                            "if": {"whitePlayerScore": 0},
                            "then": "WIN",
                            "else": "LOSS",
                        },
                    }
                }
            },
            "count": {"$sum": 1},
        }

        results = Game.objects.aggregate(
            {"$match": {"$and": [is_current_user_in_game, is_two_player_game, is_game_over]}},
            #{"$project": win_or_loss_projection},
            {"$group": group_by},
        )

        print(list(results))
        return list(results)

