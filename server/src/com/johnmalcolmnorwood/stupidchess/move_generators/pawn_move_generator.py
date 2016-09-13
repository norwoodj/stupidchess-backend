#!/usr/local/bin/python
from com.johnmalcolmnorwood.stupidchess.models.piece import PieceType
from com.johnmalcolmnorwood.stupidchess.move_generators.move_generator_utils import Offsets
from com.johnmalcolmnorwood.stupidchess.move_generators.pawn_like_move_generator import PawnLikeMoveGenerator


class PawnMoveGenerator:
    POSSIBLE_EN_PASSANT_MOVES = (
        (Offsets.LEFT_OFFSET, Offsets.LEFT_FORWARD_OFFSET),
        (Offsets.RIGHT_OFFSET, Offsets.RIGHT_FORWARD_OFFSET),
    )

    def __init__(self):
        self.__pawn_like_move_generator = PawnLikeMoveGenerator(
            directions=[Offsets.FORWARD_OFFSET],
            middle_board_forward_offset=Offsets.LEFT_OFFSET,
        )

    def get_possible_moves(self, possible_move_game_state):
        moves = self.__pawn_like_move_generator.get_possible_moves(possible_move_game_state)

        PawnMoveGenerator.__add_capturing_move(moves, Offsets.LEFT_FORWARD_OFFSET, possible_move_game_state)
        PawnMoveGenerator.__add_capturing_move(moves, Offsets.RIGHT_FORWARD_OFFSET, possible_move_game_state)

        if possible_move_game_state.is_piece_in_middle_board():
            self.__add_capturing_move(
                moves,
                Offsets.LEFT_BACKWARD_OFFSET,
                possible_move_game_state,
            )

        PawnMoveGenerator.__add_en_passant_moves(moves, possible_move_game_state)
        return moves

    @staticmethod
    def __add_capturing_move(moves, square_offset, possible_move_game_state):
        true_offset = square_offset * possible_move_game_state.get_forward_direction()
        new_square = possible_move_game_state.get_current_square() + true_offset

        if possible_move_game_state.can_capture_on_square(new_square):
            moves.append(possible_move_game_state.get_move_to_square_offset(true_offset))

    @staticmethod
    def __can_en_passant_capture_piece(capture_square, possible_move_game_state):
        piece = possible_move_game_state.get_piece_on_square(capture_square)

        if piece is None or piece.firstMove is None:
            return False

        first_move = piece.firstMove

        print(
            piece.type == PieceType.PAWN,
            first_move.gameMoveIndex == possible_move_game_state.get_last_move_index(),
            abs(first_move.destinationSquare - first_move.startSquare) == 2 * Offsets.FORWARD_OFFSET,
        )

        return (
            piece.type == PieceType.PAWN and
            first_move.gameMoveIndex == possible_move_game_state.get_last_move_index() and
            abs(first_move.destinationSquare - first_move.startSquare) == abs(2 * Offsets.FORWARD_OFFSET)
        )

    @staticmethod
    def __add_en_passant_moves(moves, possible_move_game_state):
        current_square = possible_move_game_state.get_current_square()

        for capture_offset, move_offset in PawnMoveGenerator.POSSIBLE_EN_PASSANT_MOVES:
            true_capture_offset = capture_offset * possible_move_game_state.get_forward_direction()
            true_move_offset = move_offset * possible_move_game_state.get_forward_direction()

            capture_square = current_square + true_capture_offset
            move_square = current_square + true_move_offset

            if (
                possible_move_game_state.is_square_on_board(move_square) and
                not possible_move_game_state.is_piece_on_square(move_square) and
                possible_move_game_state.can_capture_on_square(capture_square) and
                PawnMoveGenerator.__can_en_passant_capture_piece(capture_square, possible_move_game_state)
            ):
                en_passant_move = possible_move_game_state.get_move_to_square_offset(
                    true_move_offset,
                    additional_captures=[possible_move_game_state.get_piece_on_square(capture_square)],
                )

                moves.append(en_passant_move)
