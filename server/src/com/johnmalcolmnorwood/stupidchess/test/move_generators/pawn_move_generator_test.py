#!/usr/local/bin/python
from unittest import TestCase
from com.johnmalcolmnorwood.stupidchess.test import test_utils
from com.johnmalcolmnorwood.stupidchess.models.piece import Piece, PieceType, Color, FirstMove
from com.johnmalcolmnorwood.stupidchess.move_generators.pawn_move_generator import PawnMoveGenerator


class PawnMoveGeneratorTest(TestCase):
    FIRST_MOVE = FirstMove(startSquare=0, destinationSquare=10, gameMoveIndex=0)

    def test_black_no_captures_no_middle_board_first_move(self):
        pieces = [Piece(type=PieceType.PAWN, color=Color.BLACK, square=0)]
        game_state = test_utils.get_game_state(
            pieces=pieces,
        )

        move_generator = PawnMoveGenerator()
        moves = move_generator.get_possible_moves(game_state)

        self.assertEqual(len(moves), 2)
        self.assertNotEqual(moves[0].destinationSquare, moves[1].destinationSquare)
        self.assertIn(moves[0].destinationSquare, {10, 20})
        self.assertIn(moves[1].destinationSquare, {10, 20})

    def test_black_no_captures_no_middle_board_second_move(self):
        pieces = [Piece(type=PieceType.PAWN, color=Color.BLACK, square=0, firstMove=PawnMoveGeneratorTest.FIRST_MOVE)]
        game_state = test_utils.get_game_state(
            pieces=pieces,
        )

        move_generator = PawnMoveGenerator()
        moves = move_generator.get_possible_moves(game_state)

        self.assertEqual(len(moves), 1)
        self.assertEqual(moves[0].destinationSquare, 10)

    def test_black_no_captures_no_middle_board_first_move_second_move_blocked(self):
        pieces = [
            Piece(type=PieceType.PAWN, color=Color.BLACK, square=0),
            Piece(type=PieceType.PAWN, color=Color.WHITE, square=20, firstMove=PawnMoveGeneratorTest.FIRST_MOVE),
        ]

        game_state = test_utils.get_game_state(
            pieces=pieces,
        )

        move_generator = PawnMoveGenerator()
        moves = move_generator.get_possible_moves(game_state)

        self.assertEqual(len(moves), 1)
        self.assertEqual(moves[0].destinationSquare, 10)

    def test_black_no_captures_no_middle_board_first_move_first_move_blocked(self):
        pieces = [
            Piece(type=PieceType.PAWN, color=Color.BLACK, square=0),
            Piece(type=PieceType.PAWN, color=Color.WHITE, square=10, firstMove=PawnMoveGeneratorTest.FIRST_MOVE),
        ]

        game_state = test_utils.get_game_state(
            pieces=pieces,
        )

        move_generator = PawnMoveGenerator()
        moves = move_generator.get_possible_moves(game_state)

        self.assertEqual(len(moves), 0)

    def test_black_one_capture_no_middle_board(self):
        pieces = [
            Piece(type=PieceType.PAWN, color=Color.BLACK, square=0, firstMove=PawnMoveGeneratorTest.FIRST_MOVE),
            Piece(type=PieceType.PAWN, color=Color.WHITE, square=11, firstMove=PawnMoveGeneratorTest.FIRST_MOVE),
        ]

        game_state = test_utils.get_game_state(
            pieces=pieces,
        )

        move_generator = PawnMoveGenerator()
        moves = move_generator.get_possible_moves(game_state)

        self.assertEqual(len(moves), 2)
        self.assertNotEqual(moves[0].destinationSquare, moves[1].destinationSquare)
        self.assertIn(moves[0].destinationSquare, {10, 11})
        self.assertIn(moves[1].destinationSquare, {10, 11})

        capture_move = moves[0] if moves[0].destinationSquare == 11 else moves[1]
        non_capture_move = moves[0] if moves[0].destinationSquare == 10 else moves[1]
        self.assertEqual(len(capture_move.captures), 1)
        self.assertIsNone(non_capture_move.captures)

        captured_piece = capture_move.captures[0]
        self.assertEqual(captured_piece.color, Color.WHITE)
        self.assertEqual(captured_piece.type, PieceType.PAWN)

    def test_black_two_captures_no_middle_board(self):
        pieces = [
            Piece(type=PieceType.PAWN, color=Color.BLACK, square=11, firstMove=PawnMoveGeneratorTest.FIRST_MOVE),
            Piece(type=PieceType.PAWN, color=Color.WHITE, square=22, firstMove=PawnMoveGeneratorTest.FIRST_MOVE),
            Piece(type=PieceType.PAWN, color=Color.WHITE, square=20, firstMove=PawnMoveGeneratorTest.FIRST_MOVE),
            Piece(type=PieceType.PAWN, color=Color.WHITE, square=2, firstMove=PawnMoveGeneratorTest.FIRST_MOVE),
        ]

        game_state = test_utils.get_game_state(
            pieces=pieces,
            square=11,
        )

        move_generator = PawnMoveGenerator()
        moves = move_generator.get_possible_moves(game_state)

        self.assertEqual(len(moves), 3)
        self.assertIn(moves[0].destinationSquare, {20, 21, 22})
        self.assertIn(moves[1].destinationSquare, {20, 21, 22})

        capture_moves = filter(lambda move: move.destinationSquare in {20, 22}, moves)

        for non_cm in filter(lambda move: move.destinationSquare not in {20, 22}, moves):
            self.assertIsNone(non_cm.captures)

        for cm in capture_moves:
            self.assertEqual(len(cm.captures), 1)
            self.assertEqual(cm.captures[0].color, Color.WHITE)
            self.assertEqual(cm.captures[0].type, PieceType.PAWN)

    def test_black_no_captures_middle_board(self):
        pieces = [
            Piece(type=PieceType.PAWN, color=Color.BLACK, square=10, firstMove=PawnMoveGeneratorTest.FIRST_MOVE),
        ]

        game_state = test_utils.get_game_state(
            pieces=pieces,
            board_middle_section={10},
            square=10,
        )

        move_generator = PawnMoveGenerator()
        moves = move_generator.get_possible_moves(game_state)

        self.assertEqual(len(moves), 2)
        self.assertNotEqual(moves[0].destinationSquare, moves[1].destinationSquare)
        self.assertIn(moves[0].destinationSquare, {11, 20})
        self.assertIn(moves[1].destinationSquare, {11, 20})

    def test_black_captures_middle_board(self):
        pieces = [
            Piece(type=PieceType.PAWN, color=Color.BLACK, square=11, firstMove=PawnMoveGeneratorTest.FIRST_MOVE),
            Piece(type=PieceType.PAWN, color=Color.WHITE, square=20, firstMove=PawnMoveGeneratorTest.FIRST_MOVE),
            Piece(type=PieceType.PAWN, color=Color.WHITE, square=22, firstMove=PawnMoveGeneratorTest.FIRST_MOVE),
            Piece(type=PieceType.PAWN, color=Color.WHITE, square=2, firstMove=PawnMoveGeneratorTest.FIRST_MOVE),
        ]

        game_state = test_utils.get_game_state(
            pieces=pieces,
            square=11,
            board_middle_section={11},
        )

        move_generator = PawnMoveGenerator()
        moves = move_generator.get_possible_moves(game_state)

        self.assertEqual(len(moves), 5)
        capture_moves = list(filter(lambda move: move.destinationSquare in {20, 22, 2}, moves))

        for non_cm in filter(lambda move: move.destinationSquare not in {20, 22, 2}, moves):
            self.assertIsNone(non_cm.captures)

        self.assertEqual(len(capture_moves), 3)

        for cm in capture_moves:
            self.assertEqual(len(cm.captures), 1)
            self.assertEqual(cm.captures[0].color, Color.WHITE)
            self.assertEqual(cm.captures[0].type, PieceType.PAWN)

    def test_black_en_passant_right(self):
        en_passant_first_move = FirstMove(startSquare=20, destinationSquare=0, gameMoveIndex=0)
        pieces = [
            Piece(type=PieceType.PAWN, color=Color.BLACK, square=1, firstMove=PawnMoveGeneratorTest.FIRST_MOVE),
            Piece(type=PieceType.PAWN, color=Color.WHITE, square=0, firstMove=en_passant_first_move),
        ]

        game_state = test_utils.get_game_state(
            pieces=pieces,
            square=1,
        )

        move_generator = PawnMoveGenerator()
        moves = move_generator.get_possible_moves(game_state)

        self.assertEqual(len(moves), 2)
        self.assertIn(moves[0].destinationSquare, {11, 10})
        self.assertIn(moves[1].destinationSquare, {11, 10})

        en_passant = moves[0] if moves[0].destinationSquare == 10 else moves[1]
        self.assertEqual(len(en_passant.captures), 1)
        self.assertEqual(en_passant.captures[0].type, PieceType.PAWN)
        self.assertEqual(en_passant.captures[0].color, Color.WHITE)

    def test_black_en_passant_left(self):
        en_passant_first_move = FirstMove(startSquare=22, destinationSquare=2, gameMoveIndex=0)
        pieces = [
            Piece(type=PieceType.PAWN, color=Color.BLACK, square=1, firstMove=PawnMoveGeneratorTest.FIRST_MOVE),
            Piece(type=PieceType.PAWN, color=Color.WHITE, square=2, firstMove=en_passant_first_move),
        ]

        game_state = test_utils.get_game_state(
                pieces=pieces,
                square=1,
        )

        move_generator = PawnMoveGenerator()
        moves = move_generator.get_possible_moves(game_state)

        self.assertEqual(len(moves), 2)
        self.assertIn(moves[0].destinationSquare, {11, 12})
        self.assertIn(moves[1].destinationSquare, {11, 12})

        en_passant = moves[0] if moves[0].destinationSquare == 12 else moves[1]
        self.assertEqual(len(en_passant.captures), 1)
        self.assertEqual(en_passant.captures[0].type, PieceType.PAWN)
        self.assertEqual(en_passant.captures[0].color, Color.WHITE)

    def test_black_no_en_passant_wasnt_last_move(self):
        en_passant_first_move = FirstMove(startSquare=20, destinationSquare=0, gameMoveIndex=0)
        pieces = [
            Piece(type=PieceType.PAWN, color=Color.BLACK, square=1, firstMove=PawnMoveGeneratorTest.FIRST_MOVE),
            Piece(type=PieceType.PAWN, color=Color.WHITE, square=0, firstMove=en_passant_first_move),
        ]

        game_state = test_utils.get_game_state(
            game=test_utils.get_game(last_move=1, pieces=pieces),
            square=1,
        )

        move_generator = PawnMoveGenerator()
        moves = move_generator.get_possible_moves(game_state)

        self.assertEqual(len(moves), 1)
        self.assertEqual(moves[0].destinationSquare, 11)
        self.assertIsNone(moves[0].captures)

    def test_black_no_en_passant_capture_on_destination(self):
        en_passant_first_move = FirstMove(startSquare=22, destinationSquare=2, gameMoveIndex=0)
        pieces = [
            Piece(type=PieceType.PAWN, color=Color.BLACK, square=1, firstMove=PawnMoveGeneratorTest.FIRST_MOVE),
            Piece(type=PieceType.PAWN, color=Color.WHITE, square=0, firstMove=en_passant_first_move),
            Piece(type=PieceType.CASTLE, color=Color.WHITE, square=10, firstMove=PawnMoveGeneratorTest.FIRST_MOVE),
        ]

        game_state = test_utils.get_game_state(
                pieces=pieces,
                square=1,
        )

        move_generator = PawnMoveGenerator()
        moves = move_generator.get_possible_moves(game_state)

        self.assertEqual(len(moves), 2)
        self.assertIn(moves[0].destinationSquare, {11, 10})
        self.assertIn(moves[1].destinationSquare, {11, 10})

        capture_move = moves[0] if moves[0].destinationSquare == 12 else moves[1]
        self.assertEqual(len(capture_move.captures), 1)
        self.assertEqual(capture_move.captures[0].type, PieceType.CASTLE)
        self.assertEqual(capture_move.captures[0].color, Color.WHITE)


    def test_black_no_en_passant_is_not_pawn(self):
        en_passant_first_move = FirstMove(startSquare=20, destinationSquare=0, gameMoveIndex=0)
        pieces = [
            Piece(type=PieceType.PAWN, color=Color.BLACK, square=1, firstMove=PawnMoveGeneratorTest.FIRST_MOVE),
            Piece(type=PieceType.CASTLE, color=Color.WHITE, square=0, firstMove=en_passant_first_move),
        ]

        game_state = test_utils.get_game_state(
            square=1,
            pieces=pieces,
        )

        move_generator = PawnMoveGenerator()
        moves = move_generator.get_possible_moves(game_state)

        self.assertEqual(len(moves), 1)
        self.assertEqual(moves[0].destinationSquare, 11)
        self.assertIsNone(moves[0].captures)

    def test_white_no_captures_no_middle_board_first_move(self):
        pieces = [Piece(type=PieceType.PAWN, color=Color.WHITE, square=20)]
        game_state = test_utils.get_game_state(
            square=20,
            pieces=pieces,
        )

        move_generator = PawnMoveGenerator()
        moves = move_generator.get_possible_moves(game_state)

        self.assertEqual(len(moves), 2)
        self.assertNotEqual(moves[0].destinationSquare, moves[1].destinationSquare)
        self.assertIn(moves[0].destinationSquare, {0, 10})
        self.assertIn(moves[1].destinationSquare, {0, 10})

    def test_white_no_captures_no_middle_board_second_move(self):
        pieces = [Piece(type=PieceType.PAWN, color=Color.WHITE, square=20, firstMove=PawnMoveGeneratorTest.FIRST_MOVE)]
        game_state = test_utils.get_game_state(
            pieces=pieces,
            square=20,
        )

        move_generator = PawnMoveGenerator()
        moves = move_generator.get_possible_moves(game_state)

        self.assertEqual(len(moves), 1)
        self.assertEqual(moves[0].destinationSquare, 10)

    def test_white_no_captures_no_middle_board_first_move_second_move_blocked(self):
        pieces = [
            Piece(type=PieceType.PAWN, color=Color.WHITE, square=20),
            Piece(type=PieceType.PAWN, color=Color.BLACK, square=0, firstMove=PawnMoveGeneratorTest.FIRST_MOVE),
        ]

        game_state = test_utils.get_game_state(
            pieces=pieces,
            square=20,
        )

        move_generator = PawnMoveGenerator()
        moves = move_generator.get_possible_moves(game_state)

        self.assertEqual(len(moves), 1)
        self.assertEqual(moves[0].destinationSquare, 10)

    def test_white_no_captures_no_middle_board_first_move_first_move_blocked(self):
        pieces = [
            Piece(type=PieceType.PAWN, color=Color.WHITE, square=20),
            Piece(type=PieceType.PAWN, color=Color.BLACK, square=10, firstMove=PawnMoveGeneratorTest.FIRST_MOVE),
        ]

        game_state = test_utils.get_game_state(
            pieces=pieces,
            square=20,
        )

        move_generator = PawnMoveGenerator()
        moves = move_generator.get_possible_moves(game_state)

        self.assertEqual(len(moves), 0)

    def test_white_one_capture_no_middle_board(self):
        pieces = [
            Piece(type=PieceType.PAWN, color=Color.WHITE, square=11, firstMove=PawnMoveGeneratorTest.FIRST_MOVE),
            Piece(type=PieceType.PAWN, color=Color.BLACK, square=0, firstMove=PawnMoveGeneratorTest.FIRST_MOVE),
        ]

        game_state = test_utils.get_game_state(
            pieces=pieces,
            square=11,
        )

        move_generator = PawnMoveGenerator()
        moves = move_generator.get_possible_moves(game_state)

        self.assertEqual(len(moves), 2)
        self.assertNotEqual(moves[0].destinationSquare, moves[1].destinationSquare)
        self.assertIn(moves[0].destinationSquare, {0, 1})
        self.assertIn(moves[1].destinationSquare, {0, 1})

        capture_move = moves[0] if moves[0].destinationSquare == 0 else moves[1]
        non_capture_move = moves[0] if moves[0].destinationSquare == 1 else moves[1]

        self.assertEqual(len(capture_move.captures), 1)
        self.assertIsNone(non_capture_move.captures)

        captured_piece = capture_move.captures[0]
        self.assertEqual(captured_piece.color, Color.BLACK)
        self.assertEqual(captured_piece.type, PieceType.PAWN)

    def test_white_two_captures_no_middle_board(self):
        pieces = [
            Piece(type=PieceType.PAWN, color=Color.WHITE, square=11, firstMove=PawnMoveGeneratorTest.FIRST_MOVE),
            Piece(type=PieceType.PAWN, color=Color.BLACK, square=2, firstMove=PawnMoveGeneratorTest.FIRST_MOVE),
            Piece(type=PieceType.PAWN, color=Color.BLACK, square=0, firstMove=PawnMoveGeneratorTest.FIRST_MOVE),
            Piece(type=PieceType.PAWN, color=Color.BLACK, square=20, firstMove=PawnMoveGeneratorTest.FIRST_MOVE),
        ]

        game_state = test_utils.get_game_state(
            pieces=pieces,
            square=11,
        )

        move_generator = PawnMoveGenerator()
        moves = move_generator.get_possible_moves(game_state)

        self.assertEqual(len(moves), 3)
        self.assertIn(moves[0].destinationSquare, {1, 0, 2})
        self.assertIn(moves[1].destinationSquare, {1, 0, 2})

        capture_moves = filter(lambda move: move.destinationSquare in {0, 2}, moves)

        for non_cm in filter(lambda move: move.destinationSquare not in {0, 2}, moves):
            self.assertIsNone(non_cm.captures)

        for cm in capture_moves:
            self.assertEqual(len(cm.captures), 1)
            self.assertEqual(cm.captures[0].color, Color.BLACK)
            self.assertEqual(cm.captures[0].type, PieceType.PAWN)

    def test_white_no_captures_middle_board(self):
        pieces = [
            Piece(type=PieceType.PAWN, color=Color.WHITE, square=11, firstMove=PawnMoveGeneratorTest.FIRST_MOVE),
        ]

        game_state = test_utils.get_game_state(
            pieces=pieces,
            board_middle_section={11},
            square=11,
        )

        move_generator = PawnMoveGenerator()
        moves = move_generator.get_possible_moves(game_state)

        self.assertEqual(len(moves), 2)
        self.assertNotEqual(moves[0].destinationSquare, moves[1].destinationSquare)
        self.assertIn(moves[0].destinationSquare, {10, 1})
        self.assertIn(moves[1].destinationSquare, {10, 1})

    def test_white_captures_middle_board(self):
        pieces = [
            Piece(type=PieceType.PAWN, color=Color.WHITE, square=11, firstMove=PawnMoveGeneratorTest.FIRST_MOVE),
            Piece(type=PieceType.PAWN, color=Color.BLACK, square=2, firstMove=PawnMoveGeneratorTest.FIRST_MOVE),
            Piece(type=PieceType.PAWN, color=Color.BLACK, square=0, firstMove=PawnMoveGeneratorTest.FIRST_MOVE),
            Piece(type=PieceType.PAWN, color=Color.BLACK, square=20, firstMove=PawnMoveGeneratorTest.FIRST_MOVE),
        ]

        game_state = test_utils.get_game_state(
            pieces=pieces,
            square=11,
            board_middle_section={11},
        )

        move_generator = PawnMoveGenerator()
        moves = move_generator.get_possible_moves(game_state)

        self.assertEqual(len(moves), 5)

        for non_cm in filter(lambda move: move.destinationSquare not in {20, 0, 2}, moves):
            self.assertIsNone(non_cm.captures)

        capture_moves = list(filter(lambda move: move.destinationSquare in {20, 0, 2}, moves))
        self.assertEqual(len(capture_moves), 3)

        for cm in capture_moves:
            self.assertEqual(len(cm.captures), 1)
            self.assertEqual(cm.captures[0].color, Color.BLACK)
            self.assertEqual(cm.captures[0].type, PieceType.PAWN)

    def test_white_en_passant_left(self):
        en_passant_first_move = FirstMove(startSquare=1, destinationSquare=21, gameMoveIndex=0)
        pieces = [
            Piece(type=PieceType.PAWN, color=Color.WHITE, square=22, firstMove=PawnMoveGeneratorTest.FIRST_MOVE),
            Piece(type=PieceType.PAWN, color=Color.BLACK, square=21, firstMove=en_passant_first_move),
        ]

        game_state = test_utils.get_game_state(
            pieces=pieces,
            square=22,
        )

        move_generator = PawnMoveGenerator()
        moves = move_generator.get_possible_moves(game_state)

        self.assertEqual(len(moves), 2)
        self.assertIn(moves[0].destinationSquare, {11, 12})
        self.assertIn(moves[1].destinationSquare, {11, 12})

        en_passant = moves[0] if moves[0].destinationSquare == 11 else moves[1]
        self.assertEqual(len(en_passant.captures), 1)
        self.assertEqual(en_passant.captures[0].type, PieceType.PAWN)
        self.assertEqual(en_passant.captures[0].color, Color.BLACK)

    def test_white_en_passant_right(self):
        en_passant_first_move = FirstMove(startSquare=3, destinationSquare=23, gameMoveIndex=0)
        pieces = [
            Piece(type=PieceType.PAWN, color=Color.WHITE, square=22, firstMove=PawnMoveGeneratorTest.FIRST_MOVE),
            Piece(type=PieceType.PAWN, color=Color.BLACK, square=23, firstMove=en_passant_first_move),
        ]

        game_state = test_utils.get_game_state(
                pieces=pieces,
                square=22,
        )

        move_generator = PawnMoveGenerator()
        moves = move_generator.get_possible_moves(game_state)

        self.assertEqual(len(moves), 2)
        self.assertIn(moves[0].destinationSquare, {13, 12})
        self.assertIn(moves[1].destinationSquare, {13, 12})

        en_passant = moves[0] if moves[0].destinationSquare == 13 else moves[1]
        self.assertEqual(len(en_passant.captures), 1)
        self.assertEqual(en_passant.captures[0].type, PieceType.PAWN)
        self.assertEqual(en_passant.captures[0].color, Color.BLACK)
