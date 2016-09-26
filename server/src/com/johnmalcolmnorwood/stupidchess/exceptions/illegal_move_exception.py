#!/usr/local/bin/python


class IllegalMoveException(Exception):
    def __init__(self, move):
        self.move = move

