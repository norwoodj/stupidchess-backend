#!/usr/local/bin/python


class PieceType:
    KING = 'KING'
    QUEEN = 'QUEEN'


PIECE_TYPE_REGEX = '{}|{}'.format(PieceType.KING, PieceType.QUEEN)
