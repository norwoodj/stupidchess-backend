#!/usr/local/bin/python
from .. import LOGGER
from ..exceptions import InvalidMoveException
from ..models.move import Move, MoveType
from ..models.piece import Piece
from .abstract_move_update_service import AbstractMoveUpdateService
from ..utils.game_rules import is_square_in_setup_zone_for_color


class PlaceMoveUpdateService(AbstractMoveUpdateService):
    def __init__(self, game_service):
        self.__game_service = game_service

    def get_move_type(self):
        return MoveType.PLACE

    def get_moves_to_apply(self, move, game, user_uuid):
        if move.destinationSquare not in game.squaresToBePlaced:
            raise InvalidMoveException(move, f"Square {move.destinationSquare} is not available to be placed!")

        if not any(p == move.piece for p in game.possiblePiecesToBePlaced):
            LOGGER.error(f"Attempted to apply invalid PLACE move {m} on game {game.get_id()}, no matching piece in possiblePiecesToBePlaced")
            raise InvalidMoveException(move, "No such piece available to replace!")

        if not is_square_in_setup_zone_for_color(move.piece.color, move.destinationSquare):
            raise InvalidMoveException(move, f"{move.piece.color} pieces cannot be placed at {move.destinationSquare}!")

        additional_necessary_placements = self.__get_additional_necessary_placements(move, game)
        return [move, *additional_necessary_placements]

    def apply_game_updates_for_moves(self, moves, game):
        square_removals = [move.destinationSquare for move in moves]
        piece_removals = PlaceMoveUpdateService.__get_piece_removal_for_place_moves(moves, moves[0].piece.color)
        piece_additions = [PlaceMoveUpdateService.__get_piece_addition_for_move(move) for move in moves]

        updates = {
            "$pull": {
                "squaresToBePlaced": {"$in": square_removals},
                "possiblePiecesToBePlaced": piece_removals,
            },
            "$push": {
                "pieces": {"$each": piece_additions},
            },
            "$inc": {"lastMove": len(moves)},
            "$currentDate": {"lastUpdateTimestamp": True},
        }

        self.__game_service.update_game(game.get_id(), updates)

    def get_move_for_insert(self, move):
        move_piece = Piece(
            color=move.piece.color,
            type=move.piece.type,
        )

        return Move(
            type=MoveType.PLACE,
            gameUuid=move.gameUuid,
            destinationSquare=move.destinationSquare,
            index=move.index,
            piece=move_piece,
        )

    @staticmethod
    def __get_piece_removal_for_place_moves(moves, color):
        return {
            "$and": [
                {"color": color},
                {"$or": [
                    move.piece.to_dict("type", "index") for move in moves
                ]},
            ],
        }

    @staticmethod
    def __get_piece_addition_for_move(move):
        return Piece(
            color=move.piece.color,
            type=move.piece.type,
            square=move.destinationSquare,
        ).to_dict("color", "type", "square")

    def __get_additional_necessary_placements(self, last_move, game):
        """
        Applies any additional place moves if they are inevitable, for instance, if there are only pieces of a single type
        remaining, or if the user has only one piece left to place, the user has no choice where things are going to be placed
        so it may as well happen automatically

        :param game: The game to which moves are being applied
        :param last_move: The move that was just performed
        """
        piece_color = last_move.piece.color

        players_other_pieces = [
            p for p in game.possiblePiecesToBePlaced if p.color == piece_color and p.index != last_move.piece.index
        ]

        players_other_squares = [
            s for s in game.squaresToBePlaced if (
                s != last_move.destinationSquare and is_square_in_setup_zone_for_color(piece_color, s)
            )
        ]

        # See if the only remaining pieces for that color are of the same type, then they can all be
        # placed in remaining spots for the user
        piece_type = players_other_pieces[0].type

        if not all(p.type == piece_type for p in players_other_pieces):
            return []

        return PlaceMoveUpdateService.__build_place_moves_for_pieces(players_other_pieces, players_other_squares)

    @staticmethod
    def __build_place_moves_for_pieces(placers_other_pieces, players_other_squares):
        def build_move(idx, piece):
            return Move(
                type=MoveType.PLACE,
                piece=piece,
                destinationSquare=players_other_squares[idx],
            )

        return [
            build_move(idx, piece) for idx, piece in enumerate(placers_other_pieces)
        ]

