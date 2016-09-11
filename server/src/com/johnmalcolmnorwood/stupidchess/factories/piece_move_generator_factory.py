#!/usr/local/bin/python
from com.johnmalcolmnorwood.stupidchess.models.piece import PieceType
from com.johnmalcolmnorwood.stupidchess.move_generators.offset_list_move_generator import OffsetListMoveGenerator
from com.johnmalcolmnorwood.stupidchess.move_generators.directional_move_generator import DirectionalMoveGenerator


KING_OFFSETS = (-10, -9, 1, 11, 10, 9, -1, -11)
PONY_OFFSETS = (-19, -8, 12, 21, 19, 8, -12, -21)

BISHOP_DIRECTIONS = (-11, -9, 11, 9)
CASTLE_DIRECTIONS = (-10, 1, 10, -1)
QUEEN_DIRECTIONS = BISHOP_DIRECTIONS + CASTLE_DIRECTIONS

PIECE_MOVE_GENERATOR_FOR_PIECE_TYPE = {
    PieceType.KING: lambda game_state: OffsetListMoveGenerator(game_state, KING_OFFSETS),
    PieceType.QUEEN: lambda game_state: DirectionalMoveGenerator(game_state, QUEEN_DIRECTIONS),
    PieceType.BISHOP: lambda game_state: DirectionalMoveGenerator(game_state, BISHOP_DIRECTIONS),
    PieceType.CASTLE: lambda game_state: DirectionalMoveGenerator(game_state, CASTLE_DIRECTIONS),
    PieceType.PONY: lambda game_state: OffsetListMoveGenerator(game_state, PONY_OFFSETS),
}


def get_piece_move_generator_for_piece(piece_type, possible_move_game_state):
    piece_move_generator_function = PIECE_MOVE_GENERATOR_FOR_PIECE_TYPE.get(piece_type)
    return piece_move_generator_function(possible_move_game_state) if piece_move_generator_function else None
