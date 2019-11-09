#!/usr/local/bin/python
from mongoengine import StringField, IntField, EmbeddedDocumentListField, ListField
from .dictable import Dictable
from .piece import Piece, COLOR_REGEX
from .base_document import BaseDocument
from ..utils import UUID_REGEX


class GameAuthType:
    ONE_PLAYER = "ONE_PLAYER"
    TWO_PLAYER = "TWO_PLAYER"

    @staticmethod
    def all():
        return [
            GameAuthType.ONE_PLAYER,
            GameAuthType.TWO_PLAYER,
        ]


class GameType:
    STUPID_CHESS = "STUPID_CHESS"
    CHESS = "CHESS"
    CHECKERS = "CHECKERS"

    @staticmethod
    def all():
        return [
            GameType.STUPID_CHESS,
            GameType.CHESS,
            GameType.CHECKERS,
        ]


class GameResult:
    WIN = "WIN"
    LOSS = "LOSS"


GAME_TYPE_REGEX = "|".join(GameType.all())


class Game(BaseDocument, Dictable):
    meta = {
        "indexes": [
            {"fields": ("blackPlayerUuid", "lastUpdateTimestamp")},
            {"fields": ("whitePlayerUuid", "lastUpdateTimestamp")},
        ],
    }

    type = StringField(required=True, regex=GAME_TYPE_REGEX)
    lastMove = IntField(required=True, default=-1)
    pieces = EmbeddedDocumentListField(document_type=Piece, default=list)
    captures = EmbeddedDocumentListField(document_type=Piece, default=list)
    currentTurn = StringField(required=True, regex=COLOR_REGEX)
    possiblePiecesToBePlaced = EmbeddedDocumentListField(document_type=Piece, default=list)
    squaresToBePlaced = ListField(field=IntField(), default=list)
    blackPlayerUuid = StringField(required=True, regex=UUID_REGEX)
    whitePlayerUuid = StringField(required=True, regex=UUID_REGEX)
    blackPlayerName = StringField(required=True)
    whitePlayerName = StringField(required=True)
    blackPlayerScore = IntField(required=True)
    whitePlayerScore = IntField(required=True)
