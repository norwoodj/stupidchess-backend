#!/usr/local/bin/python
from mongoengine import StringField, IntField, EmbeddedDocumentField, ListField
from com.johnmalcolmnorwood.stupidchess.models.piece import Piece
from com.johnmalcolmnorwood.stupidchess.models.base_document import BaseDocument


class MoveType:
    PLACE = 'PLACE'
    MOVE = 'MOVE'


MOVE_TYPE_REGEX = '|'.join([MoveType.PLACE, MoveType.MOVE])


class Move(BaseDocument):
    type = StringField(required=True, regex=MOVE_TYPE_REGEX)
    startSquare = IntField()
    destinationSquare = IntField(required=True)
    index = IntField(required=True)
    piece = EmbeddedDocumentField(Piece)
    captures = ListField(EmbeddedDocumentField(Piece), default=None)
    gameUuid = StringField(required=True)

    @staticmethod
    def from_json(json, **kwargs):
        return Move(
            type=json.get('type'),
            startSquare=json.get('startSquare'),
            destinationSquare=json.get('destinationSquare'),
            piece=Piece.from_json(json.get('piece'))
        )
