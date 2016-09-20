#!/usr/local/bin/python
from collections import defaultdict


class AmbiguousMoveService:
    def get_ambiguous_moves(self, possible_moves):
        moves_by_destination = defaultdict(list)

        for m in possible_moves:
            moves_by_destination[m.destinationSquare].append(m)

        def filter_ambiguous(destination_move_list_pair)
        ambiguous_moves_by_destination = filter(lambda (destination, move_list): len(move_list) > 1, moves_by_destination)

        if not any(map(lambda move_list: , moves_by_destination.values())):
            return []

        caputures_by_destination_square

    @staticmethod
    def __filter_ambiguous_moves
