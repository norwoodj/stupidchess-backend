#!/usr/local/bin/python
from com.johnmalcolmnorwood.stupidchess.models.piece import PieceType


class CheckerMoveGenerator:
    def get_possible_moves(self, possible_move_game_state):
        moves = []

        PawnMoveGenerator.add_non_capturing_move(moves, PawnMoveGenerator.FORWARD_ONE_OFFSET, possible_move_game_state)
        PawnMoveGenerator.add_non_capturing_move(moves, PawnMoveGenerator.FORWARD_ONE_OFFSET, possible_move_game_state)

        # If the first step forward wasn't blocked and this piece hasn't moved yet, see if move forward two
        if not possible_move_game_state.has_piece_moved() and len(moves) > 0:
            self.add_non_capturing_move(moves, PawnMoveGenerator.FORWARD_TWO_OFFSET, possible_move_game_state)

        PawnMoveGenerator.add_capturing_move(moves, PawnMoveGenerator.DIAGONAL_RIGHT_OFFSET, possible_move_game_state)
        PawnMoveGenerator.add_capturing_move(moves, PawnMoveGenerator.DIAGONAL_LEFT_OFFSET, possible_move_game_state)

        if possible_move_game_state.is_square_in_middle_board(possible_move_game_state.get_current_square()):
            self.add_non_capturing_move(
                    moves,
                    PawnMoveGenerator.MIDDLE_BOARD_FORWARD_OFFSET,
                    possible_move_game_state,
            )

            self.add_capturing_move(
                    moves,
                    PawnMoveGenerator.MIDDLE_BOARD_DIAGONAL_OFFSET,
                    possible_move_game_state,
            )

        PawnMoveGenerator.add_en_passant_moves(moves, possible_move_game_state)

        return moves

    @staticmethod
    def add_non_capturing_move(moves, square_offset, possible_move_game_state):
        true_offset = square_offset * possible_move_game_state.get_forward_direction()
        new_square = possible_move_game_state.get_current_square() + true_offset

        if not possible_move_game_state.is_piece_on_square(new_square):
            moves.append(possible_move_game_state.get_move_to_square_offset(true_offset))

    @staticmethod
    def add_capturing_move(moves, square_offset, possible_move_game_state):
        true_offset = square_offset * possible_move_game_state.get_forward_direction()
        new_square = possible_move_game_state.get_current_square() + true_offset

        if possible_move_game_state.can_capture_on_square(new_square):
            moves.append(possible_move_game_state.get_move_to_square_offset(true_offset))

    @staticmethod
    def can_en_passant_capture_piece(piece, possible_move_game_state):
        if piece is None or piece.firstMove is None:
            return False

        first_move = piece.firstMove
        print(abs(first_move.destinationSquare - first_move.startSquare))

        return (
            piece.type == PieceType.PAWN and
            first_move.gameMoveIndex == possible_move_game_state.get_last_move_index() and
            abs(first_move.destinationSquare - first_move.startSquare) == PawnMoveGenerator.FORWARD_TWO_OFFSET
        )

    @staticmethod
    def add_en_passant(moves, possible_move_game_state):
        current_square = possible_move_game_state.get_current_square()

        for capture_offset, move_offset in PawnMoveGenerator.POSSIBLE_EN_PASSANT_MOVES:
            capture_piece = possible_move_game_state.get_piece_on_square(current_square + capture_offset)
            move_square = current_square + move_offset

            if (
                            possible_move_game_state.is_square_on_board(move_square) and
                            not possible_move_game_state.is_piece_on_square(move_square) and
                        PawnMoveGenerator.can_en_passant_capture_piece(capture_piece, possible_move_game_state)
            ):
                en_passant_move = possible_move_game_state.get_move_to_square_offset(
                        PawnMoveGenerator.DIAGONAL_LEFT_OFFSET,
                        additional_captures=[capture_piece],
                )

                moves.append(en_passant_move)
