#!/usr/local/bin/python


class GameType:
    STUPID_CHESS = 'STUPID_CHESS'
    CHESS = 'CHESS'
    CHECKERS = 'CHECKERS'

GAME_TYPE_REGEX = '{}|{}|{}'.format(
    GameType.STUPID_CHESS,
    GameType.CHESS,
    GameType.CHECKERS,
)

