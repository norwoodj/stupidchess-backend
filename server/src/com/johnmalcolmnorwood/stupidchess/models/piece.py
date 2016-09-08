#!/usr/local/bin/python
from mongoengine import EmbeddedDocument, IntField, StringField


class Color:
    BLACK = 'BLACK'
    WHITE = 'WHITE'


COLOR_REGEX = '{}|{}'.format(Color.BLACK, Color.WHITE)


class PieceType:
    KING = 'KING'
    QUEEN = 'QUEEN'


PIECE_TYPE_REGEX = '{}|{}'.format(PieceType.KING, PieceType.QUEEN)


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
