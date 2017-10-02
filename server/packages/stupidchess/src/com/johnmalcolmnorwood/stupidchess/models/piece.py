#!/usr/local/bin/python
from mongoengine import EmbeddedDocument, IntField, StringField, EmbeddedDocumentField
from .dictable import Dictable


class Color:
    BLACK = 'BLACK'
    WHITE = 'WHITE'


COLOR_REGEX = '|'.join([Color.BLACK, Color.WHITE])


class PieceType:
    KING = 'KING'
    QUEEN = 'QUEEN'
    BISHOP = 'BISHOP'
    CASTLE = 'CASTLE'
    PONY = 'PONY'
    CHECKER = 'CHECKER'
    CHECKER_KING = 'CHECKER_KING'
    PAWN = 'PAWN'


PIECE_TYPE_REGEX = '|'.join([
    PieceType.KING,
    PieceType.QUEEN,
    PieceType.BISHOP,
    PieceType.PONY,
    PieceType.CASTLE,
    PieceType.CHECKER,
    PieceType.CHECKER_KING,
    PieceType.PAWN,
])


class FirstMove(EmbeddedDocument, Dictable):
    gameMoveIndex = IntField(required=True)
    startSquare = IntField(required=True)
    destinationSquare = IntField(required=True)


class Piece(EmbeddedDocument, Dictable):
    type = StringField(required=True, regex=PIECE_TYPE_REGEX)
    color = StringField(required=True, regex=COLOR_REGEX)
    square = IntField()
    index = IntField()
    firstMove = EmbeddedDocumentField(FirstMove)

    def __eq__(self, other):
        return all([
            self.type == other.type,
            self.color == other.color,
            self.square == other.square,
            self.index == other.index,
        ])

    @staticmethod
    def from_json(json, **kwargs):
        if json is None:
            return None

        return Piece(
            type=json.get('type'),
            color=json.get('color'),
            square=json.get('destinationSquare'),
            index=json.get('index'),
        )
