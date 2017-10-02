#!/usr/local/bin/python
from collections import defaultdict
from .. import LOGGER


class AmbiguousMoveService:
    def get_ambiguous_moves(self, possible_moves):
        LOGGER.debug([m.to_dict("destinationSquare", "captures") for m in possible_moves])
        moves_by_destination = defaultdict(list)

        for m in possible_moves:
            moves_by_destination[m.destinationSquare].append(m)

        return [
            AmbiguousMoveService.__generate_ambiguous_move(destination_square, move_list)
            for destination_square, move_list in moves_by_destination.items()
            if len(move_list) > 1 and all(m.captures is not None for m in move_list)
        ]

    @staticmethod
    def __generate_ambiguous_move(destination_square, move_list):
        capture_in_other_move = {}
        for move in move_list:
            for capture in move.captures:
                if capture.square in capture_in_other_move:
                    capture_in_other_move[capture.square] = True
                else:
                    capture_in_other_move[capture.square] = False

        disambiguating_squares = [
            capture_square for capture_square, in_other_move in capture_in_other_move.items() if not in_other_move
        ]

        return {
            'destinationSquare': destination_square,
            'disambiguatingCaptures': disambiguating_squares,
        }
