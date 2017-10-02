#!/usr/local/bin/python


class InvalidMoveException(Exception):
    def __init__(self, move, reason):
        self.move = move
        self.reason = reason


class ForbiddenMoveException(Exception):
    def __init__(self, move):
        self.move = move


class InvalidGameParameterException(Exception):
    def __init__(self, message):
        self.message = message
