#!/usr/local/bin/python
from com.johnmalcolmnorwood.stupidchess.models.game import Game, GameType
from com.johnmalcolmnorwood.stupidchess.models.piece import Color
from com.johnmalcolmnorwood.stupidchess.move_generators.possible_move_game_state import PossibleMoveGameState


def get_board(rows=8, columns=8, **kwargs):
    return {r * 10 + c for c in range(columns) for r in range(rows)}


def get_game(
    game_type=GameType.STUPID_CHESS,
    pieces=[],
    last_move=0,
    pieces_to_be_placed=[],
    squares_to_be_placed=[],
    current_turn=Color.BLACK,
    black_score=1,
    white_score=1,
    **kwargs
):
    return Game(
        type=game_type,
        pieces=pieces,
        lastMove=last_move,
        possiblePiecesToBePlaced=pieces_to_be_placed,
        squaresToBePlaced=squares_to_be_placed,
        currentTurn=Color.BLACK,
        blackScore=black_score,
        whiteScore=white_score,
    )


def get_game_state(
    game=None,
    board=None,
    board_middle_section=set(),
    square=0,
    can_capture_own_pieces=False,
    check=False,
    can_checkers_move_twice_on_first_move=False,
    **kwargs
):
    game = game or get_game(**kwargs)
    board = board or get_board(**kwargs)

    return PossibleMoveGameState(
        game,
        square,
        board_square_set=board,
        board_middle_section=board_middle_section,
        can_capture_own_pieces=can_capture_own_pieces,
        check=check,
        can_checkers_move_twice_on_first_move=can_checkers_move_twice_on_first_move,
    )
