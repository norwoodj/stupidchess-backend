#!/usr/bin/env python
from functools import partial
from tabulate import tabulate
from com.johnmalcolmnorwood.stupidchess.models.game import GameType
from com.johnmalcolmnorwood.stupidchess.models.piece import Color, PieceType
from com.johnmalcolmnorwood.stupidchess.utils.game_rules import BOARD_SHAPE_FOR_GAME_TYPE

_print_no_nl = partial(print, end="")
_stupidchess_capture_grid_shape = [
    [0, 1, 2, 3, None, None, 12, 13, 14, 15],
    [4, 5, 6, 7, None, None, 16, 17, 18, 19],
    [8, 9, 10, 11, None, None, 20, 21, 22, 23],
]

_chess_capture_grid_shape = [
    [0, 1, 2, 3, 4, 5, None, None, 18, 19, 20, 21, 22, 23],
    [6, 7, 8, 9, 10, 11, None, None, 24, 25, 26, 27, 28, 29],
    [12, 13, 14, 15, 16, 17, None, None, 30, 31, 32, 33, 34, 35],
]

_capture_grid_shape_for_game_type = {
    GameType.STUPID_CHESS: _stupidchess_capture_grid_shape,
    GameType.CHESS: _chess_capture_grid_shape,
    GameType.CHECKERS: _chess_capture_grid_shape,
}

_piece_label_map = {
    PieceType.KING: "Kng",
    PieceType.QUEEN: "Qun",
    PieceType.CASTLE: "Cas",
    PieceType.BISHOP: "Bis",
    PieceType.PONY: "Pny",
    PieceType.CHECKER_KING: "CKn",
    PieceType.CHECKER: "Che",
    PieceType.PAWN: "Paw",
}


def get_white_capture_grid_starting_count(game_type):
    return 12 if game_type == GameType.STUPID_CHESS else 18


def first_square_non_null(row):
    return len(row) > 0 and row[0] is not None


def print_board_row_leading_ws():
    _print_no_nl("  ")


def print_board_row_leading_character(leading_left_wall):
    if leading_left_wall:
        _print_no_nl("|")
    else:
        _print_no_nl(" ")


def print_square_top(square, leading_none, non_null_square_above, last_non_null_square_above):
    if leading_none and non_null_square_above and not last_non_null_square_above:
        _print_no_nl("|")
    elif leading_none and square is not None and not non_null_square_above:
        _print_no_nl(" ")

    if non_null_square_above:
        _print_no_nl("_____|")
    elif square is not None:
        _print_no_nl("_____ ")
    elif square is None and (not leading_none or last_non_null_square_above):
        _print_no_nl("     ")
    else:
        _print_no_nl("      ")


def get_piece_cell(piece):
    if piece is None:
        return "     "

    color_char = " " if piece["color"] == Color.WHITE else "="
    return f"{color_char}{_piece_label_map[piece['type']]}{color_char}"


def print_row_top(row, last_row):
    print_board_row_leading_ws()

    non_null_square_above = (
        last_row is not None and
        len(last_row) > 0 and
        last_row[0] is not None
    )

    print_board_row_leading_character(non_null_square_above)
    leading_none = False
    last_non_null_square_above = False

    for idx, square in enumerate(row):
        non_null_square_above = (
            last_row is not None and
            len(last_row) > idx and
            last_row[idx] is not None
        )

        print_square_top(square, leading_none, non_null_square_above, last_non_null_square_above)
        leading_none = square is None
        last_non_null_square_above = non_null_square_above

    print()


def print_row_around_piece(row):
    print_board_row_leading_ws()
    print_board_row_leading_character(first_square_non_null(row))
    leading_none = False

    for square in row:
        if square is None:
            if leading_none:
                _print_no_nl("      ")
            else:
                _print_no_nl("     ")

            leading_none = True
        else:
            if leading_none:
                _print_no_nl("|     |")
            else:
                _print_no_nl("     |")

            leading_none = False

    print()


def print_piece_row(row, pieces):
    print_board_row_leading_ws()
    print_board_row_leading_character(first_square_non_null(row))
    leading_none = False

    for square in row:
        if square is None:
            if leading_none:
                _print_no_nl("      ")
            else:
                _print_no_nl("     ")

            leading_none = True
        else:
            pieces_on_square = [p for p in pieces if p["square"] == square]
            piece = None if len(pieces_on_square) == 0 else pieces_on_square[0]
            piece_cell = get_piece_cell(piece)
            if leading_none:
                _print_no_nl(f"|{piece_cell}|")
            else:
                _print_no_nl(f"{piece_cell}|")

            leading_none = False

    print()


def print_row(pieces, row, last_row):
    print_row_top(row, last_row)
    print_row_around_piece(row)
    print_piece_row(row, pieces)


def print_piece_grid(shape, pieces):
    last_row = None

    for next_row_idx, row in enumerate(shape, start=1):
        print_row(pieces, row, last_row)
        last_row = row

    print_row_top([None] * len(last_row), last_row)
    print()


def print_board(game):
    board_shape = BOARD_SHAPE_FOR_GAME_TYPE[game["type"]]
    pieces = game["pieces"]
    print_piece_grid(board_shape, pieces)


def print_captures(game):
    capture_shape =_capture_grid_shape_for_game_type[game["type"]]
    pieces = []
    black_count = 0
    white_count = get_white_capture_grid_starting_count(game["type"])

    for c in game["captures"]:
        if c["color"] == Color.BLACK:
            count = black_count
            black_count += 1
        else:
            count = white_count
            white_count += 1

        pieces.append({
            "square": count,
            **c,
        })

    print("Captures")
    print("--------")
    print_piece_grid(capture_shape, pieces)


def print_scoreboard(game):
    current_turn = game["currentTurn"]

    player_data = [
        ["Color", Color.BLACK, Color.WHITE],
        ["Score", game["blackPlayerScore"], game["whitePlayerScore"]],
        ["Current Turn", "*" if current_turn == Color.BLACK else "", "*" if current_turn == Color.WHITE else ""],
    ]

    table = tabulate(player_data, headers=["", game["blackPlayerName"], game["whitePlayerName"]])

    print()
    print(table)
    print()
