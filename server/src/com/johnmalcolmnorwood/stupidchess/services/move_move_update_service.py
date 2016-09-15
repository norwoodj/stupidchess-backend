#!/usr/local/bin/python
from com.johnmalcolmnorwood.stupidchess.models.move import MoveType
from com.johnmalcolmnorwood.stupidchess.models.game import Game
from com.johnmalcolmnorwood.stupidchess.models.piece import Color, FirstMove, Piece, PieceType
from com.johnmalcolmnorwood.stupidchess.services.abstract_move_update_service import AbstractMoveUpdateService


class MoveMoveUpdateService(AbstractMoveUpdateService):
    def __init__(self, possible_move_service):
        self.__possible_move_service = possible_move_service

    def get_move_type(self):
        return MoveType.MOVE

    def get_game_for_move(self, move, game_uuid):
        exclude_fields = [
            'createTimestamp', 'lastUpdateTimestamp'
        ]

        return Game.objects.exclude(*exclude_fields).get(_id=game_uuid)

    def get_moves_to_apply(self, move, game):
        possible_moves = self.__possible_move_service.get_possible_moves_from_square(
                move.startSquare,
                game.get_id(),
                game=game,
        )

        for m in possible_moves:
            if m.destinationSquare == move.destinationSquare:
                m.gameUuid = game.get_id()
                return [m]

        raise Exception()

    def apply_game_updates_for_moves(self, moves, game):
        move = moves[0]
        capture_dicts = list(map(lambda move: move.to_dict('color', 'type', 'square'), move.captures)) \
            if move.captures is not None \
            else None

        piece_removals = MoveMoveUpdateService.__get_piece_removals_for_move_move(move, capture_dicts)

        # Need to apply two updates because we can't add to and remove from the pieces array twice in one update
        # This one adds all of the new captures, removes the pieces that were captured and removes the piece that was
        # just moved
        update_one = {
            '$pull': {'pieces': piece_removals},
            '$currentDate': {'lastUpdateTimestamp': True},
        }

        if capture_dicts is not None:
            update_one['$push'] = {
                'captures': {'$each': capture_dicts}
            }

        Game.objects(_id=game.get_id()).update(__raw__=update_one)

        new_current_turn = Color.BLACK if game.currentTurn == Color.WHITE else Color.WHITE

        piece_addition = Piece(
                type=move.piece.type,
                color=move.piece.color,
                square=move.destinationSquare,
        )

        piece_addition.firstMove = piece_addition.firstMove if piece_addition.firstMove is not None else FirstMove(
                gameMoveIndex=game.lastMove + 1,
                startSquare=move.startSquare,
                destinationSquare=move.destinationSquare,
        )

        piece_addition_dict = piece_addition.to_dict('type', 'color', 'square', 'firstMove') \
            if piece_addition.type == PieceType.PAWN \
            else piece_addition.to_dict('type', 'color', 'square')

        # Second update sets the turn to the other player, adds the piece at it's new square, and increments the last
        # move index of the game
        update_two = {
            '$push': {'pieces': piece_addition_dict},
            '$set': {'currentTurn': new_current_turn},
            '$inc': {'lastMove': 1},
        }

        Game.objects(_id=game.get_id()).update(__raw__=update_two)

    def __get_move_for_insert(self, move):
        move_dict = move.to_dict(
                'type',
                'startSquare',
                'destinationSquare',
                'index',
                'gameUuid',
                'piece.color',
                'piece.type',
        )

        move_dict['captures'] = list(map(lambda capture: capture.to_dict('color', 'type', 'square')))
        return move_dict

    @staticmethod
    def __get_piece_removals_for_move_move(move, captures):
        captures = captures or []
        removals = [
            move.piece.to_dict('color', 'type', 'square'),
            *captures,
        ]

        return {'$or': removals}
