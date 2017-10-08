#!/usr/local/bin/python
from .. import LOGGER
from ..exceptions import InvalidMoveException
from ..models.game import Game, GameType
from ..models.move import Move, MoveType
from ..models.piece import Piece, PieceType, Color
from .abstract_move_update_service import AbstractMoveUpdateService


class ReplaceMoveUpdateService(AbstractMoveUpdateService):
    def get_move_type(self):
        return MoveType.REPLACE

    def get_moves_to_apply(self, move, game, user_uuid):
        if move.destinationSquare not in game.squaresToBePlaced:
            raise InvalidMoveException(move, f"Square {move.destinationSquare} is not available to be placed!")

        if not any(p == move.piece for p in game.possiblePiecesToBePlaced):
            LOGGER.error(f"Attempted to apply invalid REPLACE move {m} on game {game.get_id()}, no matching piece in possiblePiecesToBePlaced")
            raise InvalidMoveException(move, "No such piece available to replace!")

        if not any(p.color == move.piece.color and p.square == move.destinationSquare for p in game.pieces):
            LOGGER.error(f"Attempted to apply invalid REPLACE move {m} on game {game.get_id()}, no piece for color at square being replaced")
            raise InvalidMoveException(move, "No piece to be replaced at that square!")

        return [move]

    @staticmethod
    def __piece_affects_score(piece, game_type):
        return all([
            game_type in (GameType.CHESS, GameType.STUPID_CHESS),
            piece.type in (PieceType.CHECKER_KING, PieceType.KING),
        ])

    @staticmethod
    def __apply_remove_piece_update(move, game):
        remove_piece_updates = {
            "$pull": {
                "pieces": {"square": move.destinationSquare},
            },
            "$currentDate": {"lastUpdateTimestamp": True},
        }

        Game.objects(_id=game.get_id()).update(__raw__=remove_piece_updates)

    @staticmethod
    def __apply_replace_piece_update(move, game):
        new_current_turn = Color.BLACK if game.currentTurn == Color.WHITE else Color.WHITE
        replace_piece_updates = {
            "$set": {
                "possiblePiecesToBePlaced": [],
                "currentTurn": new_current_turn,
            },
            "$pull": {
                "squaresToBePlaced": move.destinationSquare,
            },
            "$push": {
                "pieces": {"square": move.destinationSquare, **move.piece.to_dict("color", "type")},
            },
            "$inc": {"lastMove": 1},
            "$currentDate": {"lastUpdateTimestamp": True},
        }

        if ReplaceMoveUpdateService.__piece_affects_score(move.piece, game.type):
            replace_piece_updates["$inc"][f"{move.piece.color.lower()}PlayerScore"] = 1

        Game.objects(_id=game.get_id()).update(__raw__=replace_piece_updates)

    def apply_game_updates_for_moves(self, moves, game):
        for m in moves:
            ReplaceMoveUpdateService.__apply_remove_piece_update(m, game)
            ReplaceMoveUpdateService.__apply_replace_piece_update(m, game)

    def get_move_for_insert(self, move):
        move_piece = Piece(
            color=move.piece.color,
            type=move.piece.type,
        )

        return Move(
            type=MoveType.REPLACE,
            gameUuid=move.gameUuid,
            destinationSquare=move.destinationSquare,
            index=move.index,
            piece=move_piece,
        )
