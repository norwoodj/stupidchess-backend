#!/usr/local/bin/python
from com.johnmalcolmnorwood.stupidchess.models.move import MoveType


class MoveApplicationService:
    def __init__(self, mongo_game_service, mongo_move_service):
        self.__mongo_game_service = mongo_game_service
        self.__mongo_move_service = mongo_move_service

    def apply_move(self, move, game_uuid):
        if move.type == MoveType.PLACE:
            self.__apply_place_move(move, game_uuid)

    def __apply_place_move(self, move, game_uuid):
        piece_to_be_placed_match = {
            'color': move.piece.color,
            'type': move.piece.type,
            'index': move.piece.index,
        }

        query = {
            '_id': game_uuid,
            'squaresToBePlaced': move.destinationSquare,
            'possiblePiecesToBePlaced': {'$elemMatch': piece_to_be_placed_match},
        }

        updates = {
            '$pull': {
                'squaresToBePlaced': move.destinationSquare,
                'possiblePiecesToBePlaced': piece_to_be_placed_match,
            },
            '$push': {
                'pieces': {
                    'color': move.piece.color,
                    'type': move.piece.type,
                    'square': move.destinationSquare,
                }
            },
            '$inc': {'lastMove': 1},
        }

        move.save()

        result = self.__mongo_game_service.update(
            query={'__raw__': query},
            updates={'__raw__': updates},
        )

        print(result)
