#!/usr/local/bin/python
from com.johnmalcolmnorwood.stupidchess.models.piece import PieceType
from com.johnmalcolmnorwood.stupidchess.move_generators.checker_move_generator import CheckerMoveGenerator
from com.johnmalcolmnorwood.stupidchess.move_generators.offset_list_move_generator import OffsetListMoveGenerator
from com.johnmalcolmnorwood.stupidchess.move_generators.directional_move_generator import DirectionalMoveGenerator
from com.johnmalcolmnorwood.stupidchess.move_generators.pawn_move_generator import PawnMoveGenerator
from com.johnmalcolmnorwood.stupidchess.move_generators.offsets import Offsets


KING_OFFSETS = (
    Offsets.FORWARD_OFFSET,
    Offsets.RIGHT_FORWARD_OFFSET,
    Offsets.RIGHT_OFFSET,
    Offsets.RIGHT_BACKWARD_OFFSET,
    Offsets.BACKWARD_OFFSET,
    Offsets.LEFT_BACKWARD_OFFSET,
    Offsets.LEFT_OFFSET,
    Offsets.LEFT_FORWARD_OFFSET,
)

PONY_OFFSETS = (
    2 * Offsets.FORWARD_OFFSET + Offsets.RIGHT_OFFSET,
    Offsets.FORWARD_OFFSET + 2 * Offsets.RIGHT_OFFSET,
    Offsets.BACKWARD_OFFSET + 2 * Offsets.RIGHT_OFFSET,
    2 * Offsets.BACKWARD_OFFSET + Offsets.RIGHT_OFFSET,
    2 * Offsets.BACKWARD_OFFSET + Offsets.LEFT_OFFSET,
    Offsets.BACKWARD_OFFSET + 2 * Offsets.LEFT_OFFSET,
    Offsets.FORWARD_OFFSET + 2 * Offsets.LEFT_OFFSET,
    2 * Offsets.FORWARD_OFFSET + Offsets.LEFT_OFFSET,
)

BISHOP_DIRECTIONS = (
    Offsets.RIGHT_FORWARD_OFFSET,
    Offsets.RIGHT_BACKWARD_OFFSET,
    Offsets.LEFT_BACKWARD_OFFSET,
    Offsets.LEFT_FORWARD_OFFSET,
)

CASTLE_DIRECTIONS = (
    Offsets.FORWARD_OFFSET,
    Offsets.RIGHT_OFFSET,
    Offsets.BACKWARD_OFFSET,
    Offsets.LEFT_OFFSET,
)

QUEEN_DIRECTIONS = BISHOP_DIRECTIONS + CASTLE_DIRECTIONS

CHECKER_OFFSETS = (
    Offsets.RIGHT_FORWARD_OFFSET,
    Offsets.LEFT_FORWARD_OFFSET,
)

CHECKER_KING_OFFSETS = (
    Offsets.RIGHT_FORWARD_OFFSET,
    Offsets.RIGHT_BACKWARD_OFFSET,
    Offsets.LEFT_BACKWARD_OFFSET,
    Offsets.LEFT_FORWARD_OFFSET,
)

PIECE_MOVE_GENERATOR_FOR_PIECE_TYPE = {
    PieceType.KING: OffsetListMoveGenerator(KING_OFFSETS),
    PieceType.QUEEN: DirectionalMoveGenerator(QUEEN_DIRECTIONS),
    PieceType.BISHOP: DirectionalMoveGenerator(BISHOP_DIRECTIONS),
    PieceType.CASTLE: DirectionalMoveGenerator(CASTLE_DIRECTIONS),
    PieceType.PONY: OffsetListMoveGenerator(PONY_OFFSETS),
    PieceType.CHECKER_KING: CheckerMoveGenerator(CHECKER_KING_OFFSETS),
    PieceType.CHECKER: CheckerMoveGenerator(CHECKER_OFFSETS, middle_board_offset=Offsets.LEFT_BACKWARD_OFFSET),
    PieceType.PAWN: PawnMoveGenerator(),
}


def get_piece_move_generator_for_piece(piece_type):
    return PIECE_MOVE_GENERATOR_FOR_PIECE_TYPE.get(piece_type)
