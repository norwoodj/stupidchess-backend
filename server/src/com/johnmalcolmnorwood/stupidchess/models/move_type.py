#!/usr/local/bin/python


class MoveType:
    PLACE = 'PLACE'
    MOVE = 'MOVE'


MOVE_TYPE_REGEX = '{}|{}'.format(MoveType.PLACE, MoveType.MOVE)
