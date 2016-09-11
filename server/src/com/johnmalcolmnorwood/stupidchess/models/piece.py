#!/usr/local/bin/python
from mongoengine import EmbeddedDocument, IntField, StringField


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


class Piece(EmbeddedDocument):
    type = StringField(required=True, regex=PIECE_TYPE_REGEX)
    color = StringField(required=True, regex=COLOR_REGEX)
    square = IntField()
    index = IntField()

    @staticmethod
    def from_json(json):
        return Piece(
            type=json.get('type'),
            color=json.get('color'),
            square=json.get('destinationSquare'),
            index=json.get('index'),
        )
