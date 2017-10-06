#!/usr/local/bin/python
from .. import LOGGER
from ..exceptions import InvalidMoveException
from ..models.move import MoveType, Move
from ..models.game import Game, GameType
from ..models.piece import Color, FirstMove, Piece, PieceType
from ..utils.game_rules import is_in_piece_promotion_zone
from .abstract_move_update_service import AbstractMoveUpdateService


class MoveMoveUpdateService(AbstractMoveUpdateService):
    def __init__(self, possible_move_service):
        self.__possible_move_service = possible_move_service

    def get_move_type(self):
        return MoveType.MOVE

    @staticmethod
    def __move_matches_requested_move(requested_move, move):
        return (
            move.destinationSquare == requested_move.destinationSquare and (
                requested_move.disambiguating_capture is None or
                requested_move.disambiguating_capture in set(map(lambda c: c.square, move.captures))
            )
        )

    @staticmethod
    def __is_checker_kinged(move, game):
        return all([
            move.piece.type == PieceType.CHECKER,
            is_in_piece_promotion_zone(move.destinationSquare, game.type, move.piece.color),
        ])

    @staticmethod
    def __get_checker_king_replace_move(move, game):
        return Move(
            type=MoveType.REPLACE,
            destinationSquare=move.destinationSquare,
            piece=Piece(type=PieceType.CHECKER_KING, color=move.piece.color),
            gameUuid=game.get_id(),
        )

    def get_moves_to_apply(self, move, game):
        possible_moves = self.__possible_move_service.get_possible_moves_from_square(
            move.startSquare,
            game,
        )

        for m in possible_moves:
            if MoveMoveUpdateService.__move_matches_requested_move(move, m):
                if MoveMoveUpdateService.__is_checker_kinged(m, game):
                    LOGGER.debug(f"Move {m} on game {game.get_id()} results in a kinged checker")
                    return [m, MoveMoveUpdateService.__get_checker_king_replace_move(m, game)]

                return [m]

        LOGGER.error(f"Attempted to apply invalid move {m} on game {game.get_id()}")
        raise InvalidMoveException(move, "No such move is possible!")

    @staticmethod
    def __capture_affects_score(game_type, capture_type):
        return game_type == GameType.CHECKERS or capture_type in (PieceType.CHECKER_KING, PieceType.KING)

    @staticmethod
    def __get_score_update_increment(game_type, captures):
        if captures is None:
            return {}

        score_update = {
            "blackPlayerScore": sum(-1 for _ in (
                c for c in captures
                if c.color == Color.BLACK and MoveMoveUpdateService.__capture_affects_score(game_type, c.type)
            )),
            "whitePlayerScore": sum(-1 for _ in (
                c for c in captures
                if c.color == Color.WHITE and MoveMoveUpdateService.__capture_affects_score(game_type, c.type)
            )),
        }

        return {
            score_field: increment for score_field, increment in score_update.items() if increment != 0
        }

    @staticmethod
    def __remove_captures_and_moved_piece_update_score(game, move):
        captures = [capture.to_dict("color", "type", "square") for capture in move.captures] \
            if move.captures is not None \
            else None

        piece_removals = MoveMoveUpdateService.__get_piece_removals_for_move_move(move, captures)

        # Need to apply two updates because we can"t add to and remove from the pieces array twice in one update
        # This one adds all of the new captures, removes the pieces that were captured and removes the piece that was
        # just moved, and also updates the score
        update_one = {
            "$pull": {"pieces": piece_removals},
            "$currentDate": {"lastUpdateTimestamp": True},
        }

        if captures is not None:
            update_one["$push"] = {
                "captures": {"$each": captures}
            }

        score_updates = MoveMoveUpdateService.__get_score_update_increment(game.type, move.captures)
        if len(score_updates) != 0:
            LOGGER.debug(f"Move {move} on game {game.get_id()} results in a score update to {', '.join(score_updates.keys())}")
            update_one["$inc"] = score_updates

        Game.objects(_id=game.get_id()).update(__raw__=update_one)

    @staticmethod
    def __add_moved_piece_update_turn_increment_move_count(game, move):
        new_current_turn = Color.BLACK if game.currentTurn == Color.WHITE else Color.WHITE

        piece_addition = Piece(
            type=move.piece.type,
            color=move.piece.color,
            firstMove=move.piece.firstMove,
            square=move.destinationSquare,
        )

        piece_addition.firstMove = piece_addition.firstMove if piece_addition.firstMove is not None else FirstMove(
            gameMoveIndex=game.lastMove + 1,
            startSquare=move.startSquare,
            destinationSquare=move.destinationSquare,
        )

        first_move_fields = ("firstMove.gameMoveIndex", "firstMove.startSquare", "firstMove.destinationSquare")
        piece_addition_dict = piece_addition.to_dict("type", "color", "square", *first_move_fields)

        # Second update sets the turn to the other player, adds the piece at it"s new square, and increments the last
        # move index of the game
        update_two = {
            "$push": {"pieces": piece_addition_dict},
            "$set": {"currentTurn": new_current_turn},
            "$inc": {"lastMove": 1},
        }

        Game.objects(_id=game.get_id()).update(__raw__=update_two)

    def apply_game_updates_for_moves(self, moves, game):
        for m in moves:
            MoveMoveUpdateService.__remove_captures_and_moved_piece_update_score(game, m)
            MoveMoveUpdateService.__add_moved_piece_update_turn_increment_move_count(game, m)

    def get_move_for_insert(self, move):
        move_captures = (
            [MoveMoveUpdateService.__get_capture_piece(c) for c in move.captures]
            if move.captures is not None
            else None
        )

        move_piece = Piece(
            color=move.piece.color,
            type=move.piece.type,
        )

        return Move(
            type=MoveType.MOVE,
            gameUuid=move.gameUuid,
            startSquare=move.startSquare,
            destinationSquare=move.destinationSquare,
            index=move.index,
            piece=move_piece,
            captures=move_captures,
        )

    @staticmethod
    def __get_capture_piece(piece):
        return Piece(
            color=piece.color,
            type=piece.type,
            square=piece.square,
        )

    @staticmethod
    def __get_piece_removals_for_move_move(move, captures):
        captures = captures or []

        removals = [
            move.piece.to_dict("color", "type", "square"),
            *captures,
        ]

        return {"$or": removals}
