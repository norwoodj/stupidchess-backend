import requests


def make_move(type, color, square):
    return {
        'type': 'PLACE',
        'destinationSquare': square,
        'piece': {
            'type': type,
            'color': color,
        },
    }

STUPID_CHESS_URL = 'http://localhost/api/{endpoint}'
BLACK_SETUP_MOVES = [
    *[make_move('PAWN', 'BLACK', i) for i in range(20, 24)],
    make_move('PONY', 'BLACK', 12),
    make_move('CHECKER', 'BLACK', 11),
    make_move('CASTLE', 'BLACK', 10),
    make_move('CASTLE', 'BLACK', 13),
    make_move('BISHOP', 'BLACK', 0),
    make_move('BISHOP', 'BLACK', 3),
    make_move('QUEEN', 'BLACK', 2),
]

WHITE_SETUP_MOVES = [
    *[make_move('PAWN', 'WHITE', i) for i in range(94, 98)],
    make_move('PONY', 'WHITE', 106),
    make_move('CHECKER', 'WHITE', 105),
    make_move('CASTLE', 'WHITE', 104),
    make_move('CASTLE', 'WHITE', 107),
    make_move('BISHOP', 'WHITE', 114),
    make_move('BISHOP', 'WHITE', 117),
    make_move('QUEEN', 'WHITE', 116),
]


def create_game(stupid_chess_url):
    response = requests.post(
        url=stupid_chess_url.format(endpoint='game/'),
        json={'type': 'STUPID_CHESS'},
    )

    game_uuid = response.json()['gameUuid']
    print('Created game {}'.format(game_uuid))
    return game_uuid


def add_moves(stupid_chess_url, game_uuid, moves):
    for idx, move in enumerate(moves):
        move['piece']['index'] = idx
        endpoint = 'game/{game_uuid}/move/'.format(game_uuid=game_uuid)

        requests.post(
            url=stupid_chess_url.format(endpoint=endpoint),
            json=move,
        )


def main():
    game_uuid = create_game(STUPID_CHESS_URL)
    add_moves(STUPID_CHESS_URL, game_uuid, BLACK_SETUP_MOVES)
    add_moves(STUPID_CHESS_URL, game_uuid, WHITE_SETUP_MOVES)


if __name__ == '__main__':
    main()
