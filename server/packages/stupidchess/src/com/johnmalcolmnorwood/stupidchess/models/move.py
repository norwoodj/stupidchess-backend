#!/usr/local/bin/python
from mongoengine import StringField, IntField, EmbeddedDocumentField, ListField

from .dictable import Dictable
from .piece import Piece
from .base_document import BaseDocument
from ..utils import UUID_REGEX


class MoveType:
    PLACE = 'PLACE'
    MOVE = 'MOVE'


MOVE_TYPE_REGEX = '|'.join([MoveType.PLACE, MoveType.MOVE])


class Move(BaseDocument, Dictable):
    # This first index is how we accomplish updates to games without the possiblity of conflicts, before making a change
    # to any game state, a move is inserted, with the index of that move in terms of order in the game. We have a unique
    # index on (gameUuid, index) however so no two simultaneous writes can both write the move. One will fail on the
    # index and be effectively locked out of updating the game until it refreshes its copy of the game
    meta = {
        "indexes": [
            {
                "fields": ["gameUuid", "index"],
                "unique": True,
            }
        ],
    }

    type = StringField(required=True, regex=MOVE_TYPE_REGEX)
    startSquare = IntField()
    destinationSquare = IntField(required=True)
    index = IntField(required=True)
    piece = EmbeddedDocumentField(Piece)
    captures = ListField(EmbeddedDocumentField(Piece), default=None)
    gameUuid = StringField(required=True, regex=UUID_REGEX)

    @staticmethod
    def from_json(json, **kwargs):
        if json is None:
            return None

        return Move(
            type=json.get('type'),
            startSquare=json.get('startSquare'),
            destinationSquare=json.get('destinationSquare'),
            piece=Piece.from_json(json.get('piece'))
        )
