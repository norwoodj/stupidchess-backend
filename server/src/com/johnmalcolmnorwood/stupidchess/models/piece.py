#!/usr/local/bin/python
from mongoengine import EmbeddedDocument, IntField, StringField
from com.johnmalcolmnorwood.stupidchess.models.color import COLOR_REGEX
from com.johnmalcolmnorwood.stupidchess.models.piece_type import PIECE_TYPE_REGEX


class Piece(EmbeddedDocument):
    type = StringField(required=True, regex=PIECE_TYPE_REGEX)
    color = StringField(required=True, regex=COLOR_REGEX)
    square = IntField()
    index = IntField()
