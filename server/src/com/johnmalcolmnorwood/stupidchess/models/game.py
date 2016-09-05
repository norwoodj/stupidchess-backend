#!/usr/local/bin/python
from flask_mongoengine import Document
from mongoengine import StringField, IntField, BooleanField, EmbeddedDocumentListField, ListField
from uuid import uuid4
from com.johnmalcolmnorwood.stupidchess.models.game_type import GAME_TYPE_REGEX
from com.johnmalcolmnorwood.stupidchess.models.piece import Piece
from com.johnmalcolmnorwood.stupidchess.models.color import COLOR_REGEX


class Game(Document):
    _id = StringField(required=True, default=lambda: str(uuid4()))
    type = StringField(required=True, regex=GAME_TYPE_REGEX)
    lastMove = IntField(required=True, default=0)
    placePieceRequired = BooleanField(required=True)
    pieces = EmbeddedDocumentListField(document_type=Piece, default=list)
    captures = EmbeddedDocumentListField(document_type=Piece, default=list)
    currentTurn = StringField(required=True, regex=COLOR_REGEX)
    blackScore = IntField(required=True)
    whiteScore = IntField(required=True)
    possiblePiecesToBePlaced = EmbeddedDocumentListField(document_type=Piece, default=list)
    squaresToBePlaced = ListField(field=IntField(), default=list)
