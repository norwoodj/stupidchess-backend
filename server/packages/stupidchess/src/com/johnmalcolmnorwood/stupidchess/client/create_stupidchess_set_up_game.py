#!/usr/local/bin/python
import requests
import click


def make_move(piece_type, color, square):
    return {
        "type": "PLACE",
        "destinationSquare": square,
        "piece": {
            "type": piece_type,
            "color": color,
        },
    }

STUPID_CHESS_URL = "http://localhost/api/{endpoint}"
BLACK_SETUP_MOVES = [
    *[make_move("PAWN", "BLACK", i) for i in range(20, 24)],
    make_move("PONY", "BLACK", 12),
    make_move("CHECKER", "BLACK", 11),
    make_move("CASTLE", "BLACK", 10),
    make_move("CASTLE", "BLACK", 13),
    make_move("BISHOP", "BLACK", 0),
    make_move("BISHOP", "BLACK", 3),
    make_move("QUEEN", "BLACK", 1),
]

WHITE_SETUP_MOVES = [
    *[make_move("PAWN", "WHITE", i) for i in range(94, 98)],
    make_move("PONY", "WHITE", 106),
    make_move("CHECKER", "WHITE", 105),
    make_move("CASTLE", "WHITE", 104),
    make_move("CASTLE", "WHITE", 107),
    make_move("BISHOP", "WHITE", 114),
    make_move("BISHOP", "WHITE", 117),
    make_move("QUEEN", "WHITE", 115),
]


def create_game(stupidchess_url, username, password):
    response = requests.post(
        url=f"{stupidchess_url}/api/game/",
        json={"type": "STUPID_CHESS", "gameAuthType": "ONE_PLAYER", "otherPlayer": "john"},
        auth=(username, password),
    )

    response.raise_for_status()
    game_uuid = response.json()["gameUuid"]
    print("Created game {}".format(game_uuid))
    return game_uuid


def add_moves(stupidchess_url, game_uuid, moves, username, password):
    for idx, move in enumerate(moves):
        move["piece"]["index"] = idx

        response = requests.post(
            url=f"{stupidchess_url}/api/game/{game_uuid}/move/",
            json=move,
            auth=(username, password),
        )

        response.raise_for_status()


@click.command()
@click.option("--stupidchess", "-s", default="http://localhost")
@click.option("--username", "-u", default="veintitres")
@click.option("--password", "-p", default="password")
def main(stupidchess, username, password):
    game_uuid = create_game(stupidchess, username, password)
    add_moves(stupidchess, game_uuid, BLACK_SETUP_MOVES, username, password)
    add_moves(stupidchess, game_uuid, WHITE_SETUP_MOVES, username, password)


if __name__ == "__main__":
    main()
