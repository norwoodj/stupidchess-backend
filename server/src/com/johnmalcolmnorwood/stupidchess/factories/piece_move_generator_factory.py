#!/usr/local/bin/python
from com.johnmalcolmnorwood.stupidchess.models.piece import PieceType
from com.johnmalcolmnorwood.stupidchess.move_generators.king_move_generator import KingMoveGenerator


PIECE_MOVE_GENERATOR_FOR_PIECE_TYPE = {
    PieceType.KING: KingMoveGenerator,
}


def get_piece_move_generator_for_piece(piece, possible_move_game_state):
    piece_move_generator_class = PIECE_MOVE_GENERATOR_FOR_PIECE_TYPE.get(piece)
    return piece_move_generator_class(possible_move_game_state) if piece_move_generator_class else None
