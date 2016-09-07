#!/usr/local/bin/python
from com.johnmalcolmnorwood.stupidchess.models.move_type import MoveType


class MoveApplicationService:
    def __init__(self, mongo_game_service, mongo_move_service):
        self.__mongo_game_service = mongo_game_service
        self.__mongo_move_service = mongo_move_service

    def apply_move(self, move, game_uuid):
        if move.type == MoveType.PLACE:
            self.__apply_place_move(move, game_uuid)

    def __apply_place_move(self, move, game_uuid):
        query = {
            '__raw__': {
                '_id': game_uuid,
                'squaresToBePlaced': move.destinationSquare,
                'possiblePiecesToBePlaced': {
                    '$elemMatch': {'color': move.piece.color, 'type': move.piece.type},
                },
            },
        }

        updates = {
            '__raw__': {
                '$pull': {
                    'squaresToBePlaced.$': move.destinationSquare,
                    'possiblePiecesToBePlaced': {'$elemMatch': {'color': move.piece.color, 'type': move.piece.type},
                    },
                },
            }
        }

        self.__mongo_game_service.update(
            query=query,
            updates=
        )

