#!/usr/local/bin/python
from mongoengine import StringField, IntField, EmbeddedDocumentField
from com.johnmalcolmnorwood.stupidchess.models.move_type import MOVE_TYPE_REGEX
from com.johnmalcolmnorwood.stupidchess.models.piece import Piece
from com.johnmalcolmnorwood.stupidchess.models.base_document import BaseDocument


class Move(BaseDocument):
    type = StringField(required=True, regex=MOVE_TYPE_REGEX)
    startSquare = IntField()
    destinationSquare = IntField(required=True)
    piece = EmbeddedDocumentField(Piece)
