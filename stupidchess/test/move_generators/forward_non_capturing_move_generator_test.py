#!/usr/local/bin/python
from unittest import TestCase

from stupidchess.move_generators.offsets import Offsets
from stupidchess.test import test_utils
from stupidchess.models.piece import Piece, PieceType, Color, FirstMove
from stupidchess.move_generators.forward_non_capturing_move_generator import (
    ForwardNonCapturingMoveGenerator,
)


class ForwardNonCapturingMoveGeneratorTest(TestCase):
    FIRST_MOVE = FirstMove(startSquare=0, destinationSquare=10, gameMoveIndex=0)

    def test_black_cant_move_off_board(self):
        pieces = [
            Piece(
                type=PieceType.PAWN,
                color=Color.BLACK,
                square=70,
                firstMove=ForwardNonCapturingMoveGeneratorTest.FIRST_MOVE,
            )
        ]

        game_state = test_utils.get_game_state(
            pieces=pieces,
            square=70,
        )

        move_generator = ForwardNonCapturingMoveGenerator([Offsets.FORWARD_OFFSET], Offsets.LEFT_OFFSET)
        moves = move_generator.get_possible_moves(game_state)

        self.assertEqual(len(moves), 0)

    def test_white_cant_move_off_board(self):
        pieces = [
            Piece(
                type=PieceType.PAWN,
                color=Color.WHITE,
                square=0,
                firstMove=ForwardNonCapturingMoveGeneratorTest.FIRST_MOVE,
            )
        ]

        game_state = test_utils.get_game_state(
            pieces=pieces,
        )

        move_generator = ForwardNonCapturingMoveGenerator([Offsets.FORWARD_OFFSET], Offsets.LEFT_OFFSET)
        moves = move_generator.get_possible_moves(game_state)

        self.assertEqual(len(moves), 0)
