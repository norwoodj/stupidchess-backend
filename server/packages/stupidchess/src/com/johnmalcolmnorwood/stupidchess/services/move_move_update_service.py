#!/usr/local/bin/python
from com.johnmalcolmnorwood.stupidchess.exceptions import IllegalMoveException
from com.johnmalcolmnorwood.stupidchess.models.move import MoveType, Move
from com.johnmalcolmnorwood.stupidchess.models.game import Game
from com.johnmalcolmnorwood.stupidchess.models.piece import Color, FirstMove, Piece
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

    @staticmethod
    def __move_matches_requested_move(requested_move, move):
        return (
            move.destinationSquare == requested_move.destinationSquare and (
                requested_move.disambiguating_capture is None or
                requested_move.disambiguating_capture in set(map(lambda c: c.square, move.captures))
            )
        )

    def get_moves_to_apply(self, move, game):
        possible_moves = self.__possible_move_service.get_possible_moves_from_square(
            move.startSquare,
            game.get_id(),
            game=game,
        )

        for m in possible_moves:
            if MoveMoveUpdateService.__move_matches_requested_move(move, m):
                m.gameUuid = game.get_id()
                return [m]

        raise IllegalMoveException(move)

    def apply_game_updates_for_moves(self, moves, game):
        move = moves[0]
        captures = [capture.to_dict('color', 'type', 'square') for capture in move.captures] \
            if move.captures is not None \
            else None

        piece_removals = MoveMoveUpdateService.__get_piece_removals_for_move_move(move, captures)

        # Need to apply two updates because we can't add to and remove from the pieces array twice in one update
        # This one adds all of the new captures, removes the pieces that were captured and removes the piece that was
        # just moved
        update_one = {
            '$pull': {'pieces': piece_removals},
            '$currentDate': {'lastUpdateTimestamp': True},
        }

        if captures is not None:
            update_one['$push'] = {
                'captures': {'$each': captures}
            }

        Game.objects(_id=game.get_id()).update(__raw__=update_one)

        new_current_turn = Color.BLACK if game.currentTurn == Color.WHITE else Color.WHITE

        piece_addition = Piece(
            type=move.piece.type,
            color=move.piece.color,
            firstMove=move.piece.firstMove,
            square=move.destinationSquare,
        )

        piece_addition.firstMove = piece_addition.firstMove if piece_addition.firstMove is not None else FirstMove(
            gameMoveIndex=game.lastMove + 1,
            startSquare=move.startSquare,
            destinationSquare=move.destinationSquare,
        )

        first_move_fields = ('firstMove.gameMoveIndex', 'firstMove.startSquare', 'firstMove.destinationSquare')
        piece_addition_dict = piece_addition.to_dict('type', 'color', 'square', *first_move_fields)

        # Second update sets the turn to the other player, adds the piece at it's new square, and increments the last
        # move index of the game
        update_two = {
            '$push': {'pieces': piece_addition_dict},
            '$set': {'currentTurn': new_current_turn},
            '$inc': {'lastMove': 1},
        }

        Game.objects(_id=game.get_id()).update(__raw__=update_two)

    def get_move_for_insert(self, move):
        move_captures = list(map(MoveMoveUpdateService.__get_capture_piece, move.captures)) \
            if move.captures is not None \
            else None

        move_piece = Piece(
            color=move.piece.color,
            type=move.piece.type,
        )

        return Move(
            type=MoveType.MOVE,
            gameUuid=move.gameUuid,
            startSquare=move.startSquare,
            destinationSquare=move.destinationSquare,
            index=move.index,
            piece=move_piece,
            captures=move_captures,
        )

    @staticmethod
    def __get_capture_piece(piece):
        return Piece(
            color=piece.color,
            type=piece.type,
            square=piece.square,
        )

    @staticmethod
    def __get_piece_removals_for_move_move(move, captures):
        captures = captures or []

        removals = [
            move.piece.to_dict('color', 'type', 'square'),
            *captures,
        ]

        return {'$or': removals}
