#!/usr/local/bin/python
from unittest import TestCase

from com.johnmalcolmnorwood.stupidchess.move_generators.move_generator_utils import Offsets
from com.johnmalcolmnorwood.stupidchess.move_generators.pawn_like_move_generator import PawnLikeMoveGenerator
from com.johnmalcolmnorwood.stupidchess.test import test_utils
from com.johnmalcolmnorwood.stupidchess.models.piece import Piece, PieceType, Color, FirstMove


class PawnLikeMoveGeneratorTest(TestCase):
    FIRST_MOVE = FirstMove(startSquare=0, destinationSquare=10, gameMoveIndex=0)

    def test_black_cant_move_off_board(self):
        pieces = [
            Piece(type=PieceType.PAWN, color=Color.BLACK, square=70, firstMove=PawnLikeMoveGeneratorTest.FIRST_MOVE)
        ]

        game_state = test_utils.get_game_state(
            pieces=pieces,
            square=70,
        )

        move_generator = PawnLikeMoveGenerator([Offsets.FORWARD_OFFSET], Offsets.LEFT_OFFSET)
        moves = move_generator.get_possible_moves(game_state)

        self.assertEqual(len(moves), 0)

    def test_white_cant_move_off_board(self):
        pieces = [
            Piece(type=PieceType.PAWN, color=Color.WHITE, square=0, firstMove=PawnLikeMoveGeneratorTest.FIRST_MOVE)
        ]

        game_state = test_utils.get_game_state(
            pieces=pieces,
        )

        move_generator = PawnLikeMoveGenerator([Offsets.FORWARD_OFFSET], Offsets.LEFT_OFFSET)
        moves = move_generator.get_possible_moves(game_state)

        self.assertEqual(len(moves), 0)
