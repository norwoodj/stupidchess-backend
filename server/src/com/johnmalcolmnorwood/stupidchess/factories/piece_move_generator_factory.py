#!/usr/local/bin/python
from com.johnmalcolmnorwood.stupidchess.models.piece import PieceType
from com.johnmalcolmnorwood.stupidchess.move_generators.offset_list_move_generator import OffsetListMoveGenerator
from com.johnmalcolmnorwood.stupidchess.move_generators.directional_move_generator import DirectionalMoveGenerator
from com.johnmalcolmnorwood.stupidchess.move_generators.pawn_move_generator import PawnMoveGenerator


KING_OFFSETS = (-10, -9, 1, 11, 10, 9, -1, -11)
PONY_OFFSETS = (-19, -8, 12, 21, 19, 8, -12, -21)

BISHOP_DIRECTIONS = (-11, -9, 11, 9)
CASTLE_DIRECTIONS = (-10, 1, 10, -1)
QUEEN_DIRECTIONS = BISHOP_DIRECTIONS + CASTLE_DIRECTIONS

PIECE_MOVE_GENERATOR_FOR_PIECE_TYPE = {
    PieceType.KING: OffsetListMoveGenerator(KING_OFFSETS),
    PieceType.QUEEN: DirectionalMoveGenerator(QUEEN_DIRECTIONS),
    PieceType.BISHOP: DirectionalMoveGenerator(BISHOP_DIRECTIONS),
    PieceType.CASTLE: DirectionalMoveGenerator(CASTLE_DIRECTIONS),
    PieceType.PONY: OffsetListMoveGenerator(PONY_OFFSETS),
    PieceType.CHECKER: PawnMoveGenerator(),
    PieceType.PAWN: PawnMoveGenerator(),
}


def get_piece_move_generator_for_piece(piece_type):
    return PIECE_MOVE_GENERATOR_FOR_PIECE_TYPE.get(piece_type)
