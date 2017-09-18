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
    def create_game(game_type, game_auth_type, other_player):
        game = create_new_game(game_type, game_auth_type, other_player)
        game.save()
        return game

    @staticmethod
    def get_games_for_user(user_uuid, skip=0, results=10):
        games = Game.objects(__raw__={
            "$or": [
                {"blackPlayerUuid": user_uuid},
                {"whitePlayerUuid": user_uuid},
            ],
        })[skip: skip + results]

        return [GameService.__remove_unprivileged_moves(g, user_uuid) for g in games]

    @staticmethod
    def get_game_for_user_and_game_uuid(user_uuid, game_uuid):
        game = Game.objects.exclude("createTimestamp", "lastUpdateTimestamp").get_or_404(__raw__={
            "$and": [
                {"_id": game_uuid},
                {"$or": [{"blackPlayerUuid": user_uuid}, {"whitePlayerUuid": user_uuid}]}
            ],
        })

        return GameService.__remove_unprivileged_moves(game, user_uuid)

    def get_possible_moves(self, user_uuid, game_uuid, square):
        game = GameService.get_game_for_user_and_game_uuid(user_uuid, game_uuid)

        if not GameService.__is_players_turn(game, user_uuid):
            return []

        return self.__possible_move_service.get_possible_moves_from_square(square, game)
