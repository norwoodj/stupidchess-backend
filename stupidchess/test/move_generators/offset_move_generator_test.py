#!/usr/local/bin/python
from unittest import TestCase

from stupidchess.models.piece import Piece, PieceType, Color
from stupidchess.move_generators.offsets import Offsets
from stupidchess.move_generators.offset_list_move_generator import OffsetListMoveGenerator
from stupidchess.test import test_utils


class OffsetMoveGeneratorTest(TestCase):
    def test_forward_two_left_and_right(self):
        offsets = (
            Offsets.FORWARD_OFFSET * 2 + Offsets.RIGHT_OFFSET,
            Offsets.FORWARD_OFFSET * 2 + Offsets.LEFT_OFFSET
        )

        move_generator = OffsetListMoveGenerator(offsets)
        pieces = [Piece(type=PieceType.PONY, color=Color.BLACK, square=1)]
        game_state = test_utils.get_game_state(
            pieces=pieces,
            square=1,
        )

        moves = list(move_generator.get_possible_moves(game_state))

        self.assertEqual(len(moves), 2)
        self.assertNotEqual(moves[0].destinationSquare, moves[1].destinationSquare)
        self.assertIn(moves[0].destinationSquare, {20, 22})
        self.assertIn(moves[1].destinationSquare, {20, 22})
