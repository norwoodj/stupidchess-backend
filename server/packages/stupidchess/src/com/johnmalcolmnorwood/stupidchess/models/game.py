#!/usr/local/bin/python
from mongoengine import StringField, IntField, EmbeddedDocumentListField, ListField
from com.johnmalcolmnorwood.stupidchess.models.dictable import Dictable
from com.johnmalcolmnorwood.stupidchess.models.piece import Piece, COLOR_REGEX
from com.johnmalcolmnorwood.stupidchess.models.base_document import BaseDocument
from com.johnmalcolmnorwood.stupidchess.models import UUID_REGEX


class GameAuthType:
    ONE_PLAYER = 'ONE_PLAYER'
    TWO_PLAYER = 'TWO_PLAYER'


class GameType:
    STUPID_CHESS = 'STUPID_CHESS'
    CHESS = 'CHESS'
    CHECKERS = 'CHECKERS'


GAME_TYPE_REGEX = '|'.join([
    GameType.STUPID_CHESS,
    GameType.CHESS,
    GameType.CHECKERS,
])


class Game(BaseDocument, Dictable):
    type = StringField(required=True, regex=GAME_TYPE_REGEX)
    lastMove = IntField(required=True, default=-1)
    pieces = EmbeddedDocumentListField(document_type=Piece, default=list)
    captures = EmbeddedDocumentListField(document_type=Piece, default=list)
    currentTurn = StringField(required=True, regex=COLOR_REGEX)
    possiblePiecesToBePlaced = EmbeddedDocumentListField(document_type=Piece, default=list)
    squaresToBePlaced = ListField(field=IntField(), default=list)
    blackPlayerUuid = StringField(required=True, regex=UUID_REGEX)
    whitePlayerUuid = StringField(required=True, regex=UUID_REGEX)
