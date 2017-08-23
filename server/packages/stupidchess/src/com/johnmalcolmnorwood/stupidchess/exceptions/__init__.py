#!/usr/local/bin/python


class IllegalMoveException(Exception):
    def __init__(self, move):
        self.move = move


class InvalidGameParameterException(Exception):
    def __init__(self, message):
        self.message = message
