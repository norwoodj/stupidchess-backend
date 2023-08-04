#!/usr/local/bin/python
from ..models.piece import PieceType
from .offsets import Offsets
from .forward_non_capturing_move_generator import ForwardNonCapturingMoveGenerator


class PawnMoveGenerator:
    POSSIBLE_EN_PASSANT_MOVES = (
        (Offsets.LEFT_OFFSET, Offsets.LEFT_FORWARD_OFFSET),
        (Offsets.RIGHT_OFFSET, Offsets.RIGHT_FORWARD_OFFSET),
    )

    def __init__(self):
        self.__forward_non_capturing_move_generator = ForwardNonCapturingMoveGenerator(
            directions=[Offsets.FORWARD_OFFSET],
            middle_board_forward_offset=Offsets.LEFT_OFFSET,
        )

    def get_possible_moves(self, possible_move_game_state):
        moves = self.__forward_non_capturing_move_generator.get_possible_moves(
            possible_move_game_state
        )
        non_capturing_moves = list(filter(lambda m: m.captures is None, moves))

        if (
            len(non_capturing_moves) > 0
            and possible_move_game_state.can_piece_move_twice()
        ):
            non_capturing_move = non_capturing_moves[0]
            self.__forward_non_capturing_move_generator.add_non_capturing_move(
                moves,
                non_capturing_move.destinationSquare,
                Offsets.FORWARD_OFFSET,
                possible_move_game_state,
            )

        PawnMoveGenerator.__add_capturing_move(
            moves, Offsets.LEFT_FORWARD_OFFSET, possible_move_game_state
        )
        PawnMoveGenerator.__add_capturing_move(
            moves, Offsets.RIGHT_FORWARD_OFFSET, possible_move_game_state
        )

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
        new_square = possible_move_game_state.get_square_for_move_offset(square_offset)

        if possible_move_game_state.can_capture_on_square(new_square):
            moves.append(possible_move_game_state.get_move_to_square(new_square))

    @staticmethod
    def __can_en_passant_capture_piece(capture_square, possible_move_game_state):
        piece = possible_move_game_state.get_piece_on_square(capture_square)

        if piece is None or piece.firstMove is None:
            return False

        first_move = piece.firstMove

        return (
            piece.type == PieceType.PAWN
            and first_move.gameMoveIndex
            == possible_move_game_state.get_last_move_index()
            and abs(first_move.destinationSquare - first_move.startSquare)
            == abs(2 * Offsets.FORWARD_OFFSET)
        )

    @staticmethod
    def __add_en_passant_moves(moves, possible_move_game_state):
        for capture_offset, move_offset in PawnMoveGenerator.POSSIBLE_EN_PASSANT_MOVES:
            capture_square = possible_move_game_state.get_square_for_move_offset(
                capture_offset
            )
            move_square = possible_move_game_state.get_square_for_move_offset(
                move_offset
            )

            if (
                possible_move_game_state.is_square_on_board(move_square)
                and not possible_move_game_state.is_piece_on_square(move_square)
                and possible_move_game_state.can_capture_on_square(capture_square)
                and PawnMoveGenerator.__can_en_passant_capture_piece(
                    capture_square, possible_move_game_state
                )
            ):
                en_passant_move = possible_move_game_state.get_move_to_square(
                    move_square,
                    additional_captures=[
                        possible_move_game_state.get_piece_on_square(capture_square)
                    ],
                )

                moves.append(en_passant_move)
