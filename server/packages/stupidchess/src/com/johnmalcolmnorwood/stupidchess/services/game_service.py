#!/usr/bin/env python
from ..factories.game_factory import create_new_game
from ..models.game import Game, GameType
from ..models.piece import Color, PieceType


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
    def __get_any_pieces_left_criterium(color):
        return {"pieces": {"$elemMatch": {"color": color}}}

    @staticmethod
    def __get_no_pieces_left_criterium(color):
        return {"pieces": {"$not": {"$elemMatch": {"color": color}}}}

    @staticmethod
    def __get_any_kings_left_criterium(color):
        return {
            "pieces": {
                "$elemMatch": {
                    "color": color,
                    "type": {"$in": [PieceType.KING, PieceType.CHECKER_KING]},
                },
            },
        }

    @staticmethod
    def __get_no_kings_left_criterium(color):
        return {
            "pieces": {
                "$not": {
                    "$elemMatch": {
                        "color": color,
                        "type": {"$in": [PieceType.KING, PieceType.CHECKER_KING]},
                    },
                },
            },
        }

    @staticmethod
    def __game_active_criteria():
        all_pieces_on_neither_side_captured = {
            "$and": [
                GameService.__get_any_pieces_left_criterium(Color.BLACK),
                GameService.__get_any_pieces_left_criterium(Color.WHITE),
            ],
        }

        checkers_game_active = {"$and": [{"type": GameType.CHECKERS}, all_pieces_on_neither_side_captured]}

        in_board_setup_mode = {"$and": [{"type": GameType.STUPID_CHESS}, {"lastMove": {"$lt": 24}}]}
        all_kings_on_neither_side_captured = {
            "$and": [
                GameService.__get_any_kings_left_criterium(Color.BLACK),
                GameService.__get_any_kings_left_criterium(Color.WHITE),
            ]
        }

        chess_game_active = {
            "$and": [
                {"type": {"$in": [GameType.CHESS, GameType.STUPID_CHESS]}},
                {"$or": [in_board_setup_mode, all_kings_on_neither_side_captured]},
            ],
        }

        return {
            "$or": [
                checkers_game_active,
                chess_game_active,
            ]
        }

    @staticmethod
    def __game_over_criteria():
        all_pieces_on_one_side_captured = {
            "$or": [
                GameService.__get_no_pieces_left_criterium(Color.BLACK),
                GameService.__get_no_pieces_left_criterium(Color.WHITE),
            ],
        }

        checkers_game_over = {"$and": [{"type": GameType.CHECKERS}, all_pieces_on_one_side_captured]}
        not_in_board_setup_mode = {"$or": [{"type": {"$ne": GameType.STUPID_CHESS}}, {"lastMove": {"$gt": 23}}]}
        all_kings_on_one_side_captured = {
            "$or": [
                GameService.__get_no_kings_left_criterium(Color.BLACK),
                GameService.__get_no_kings_left_criterium(Color.WHITE),
            ]
        }

        chess_game_over = {
            "$and": [
                {"type": {"$in": [GameType.CHESS, GameType.STUPID_CHESS]}},
                {"$and": [not_in_board_setup_mode, all_kings_on_one_side_captured]},
            ],
        }

        return {
            "$or": [
                checkers_game_over,
                chess_game_over,
            ]
        }

    @staticmethod
    def __checkers_winning_condition(user_uuid):
        black_checker_wins = {
            "$and": [{"blackPlayerUuid": user_uuid}, GameService.__get_no_pieces_left_criterium(Color.WHITE)],
        }

        white_checker_wins = {
            "$and": [{"whitePlayerUuid": user_uuid}, GameService.__get_no_pieces_left_criterium(Color.BLACK)],
        }

        return {"$or": [black_checker_wins, white_checker_wins]}

    @staticmethod
    def __chess_winning_condition(user_uuid):
        black_chess_wins = {
            "$and": [{"blackPlayerUuid": user_uuid}, GameService.__get_no_kings_left_criterium(Color.WHITE)],
        }

        white_chess_wins = {
            "$and": [{"whitePlayerUuid": user_uuid}, GameService.__get_no_kings_left_criterium(Color.BLACK)],
        }

        return {"$or": [black_chess_wins, white_chess_wins]}

    @staticmethod
    def __stupidchess_winning_condition(user_uuid):
        return {
            "$and": [
                {"lastMove": {"gt": 23}},
                GameService.__chess_winning_condition(user_uuid),
            ]
        }

    @staticmethod
    def __get_winning_condition_for_game_type(user_uuid, game_type):
        winning_condition_handler_map = {
            GameType.CHECKERS: GameService.__checkers_winning_condition,
            GameType.CHESS: GameService.__chess_winning_condition,
            GameType.STUPID_CHESS: GameService.__stupidchess_winning_condition,
        }

        return winning_condition_handler_map[game_type](user_uuid)

    @staticmethod
    def __get_user_is_winner_criteria(user_uuid, game_type):
        if game_type is not None:
            return {
                "$and": [{"type": game_type}, GameService.__get_winning_condition_for_game_type(user_uuid, game_type)],
            }

        else:
            return {
                "$or": [
                    {"$and": [{"type": t}, GameService.__get_winning_condition_for_game_type(user_uuid, t)]}
                    for t in GameType.all()
                ],
            }

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
    def __query_games_for_user(user_uuid, game_type=None, extra_criteria=[]):
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
    def get_games_for_user(user_uuid, game_type=None, skip=0, results=10, extra_criteria=[]):
        games = GameService.__query_games_for_user(user_uuid, game_type, extra_criteria)
        ordered = games.order_by("-lastUpdateTimestamp")
        game_page = ordered[skip:skip+results]

        return [GameService.__remove_unprivileged_moves(g, user_uuid) for g in game_page]

    @staticmethod
    def count_games_for_user(user_uuid, game_type=None, extra_criteria=[]):
        games = GameService.__query_games_for_user(user_uuid, game_type, extra_criteria)
        return games.count()

    @staticmethod
    def count_winning_games_for_user(user_uuid, game_type=None):
        return GameService.count_games_for_user(
            user_uuid=user_uuid,
            game_type=game_type,
            extra_criteria=[GameService.__get_user_is_winner_criteria(user_uuid, game_type)],
        )

    @staticmethod
    def get_winning_games_for_user(user_uuid, game_type=None, skip=0, results=10):
        return GameService.get_games_for_user(
            user_uuid=user_uuid,
            game_type=game_type,
            skip=skip,
            results=results,
            extra_criteria=[GameService.__get_user_is_winner_criteria(user_uuid, game_type)],
        )

    @staticmethod
    def get_active_games_for_user(user_uuid, game_type=None, skip=0, results=10):
        return GameService.get_games_for_user(
            user_uuid=user_uuid,
            game_type=game_type,
            skip=skip,
            results=results,
            extra_criteria=[GameService.__game_active_criteria()],
        )

    @staticmethod
    def count_completed_games_for_user(user_uuid, game_type=None):
        return GameService.count_games_for_user(
            user_uuid=user_uuid,
            game_type=game_type,
            extra_criteria=[GameService.__game_over_criteria()],
        )

    @staticmethod
    def get_completed_games_for_user(user_uuid, game_type=None, skip=0, results=10):
        return GameService.get_games_for_user(
            user_uuid=user_uuid,
            game_type=game_type,
            skip=skip,
            results=results,
            extra_criteria=[GameService.__game_over_criteria()],
        )

    def get_possible_moves(self, user_uuid, game_uuid, square):
        game = GameService.get_game_for_user_and_game_uuid(user_uuid, game_uuid)

        if not GameService.__is_players_turn(game, user_uuid):
            return []

        return self.__possible_move_service.get_possible_moves_from_square(square, game)
