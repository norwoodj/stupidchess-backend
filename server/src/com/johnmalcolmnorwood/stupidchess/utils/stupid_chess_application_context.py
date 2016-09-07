#!/usr/local/bin/python
from com.johnmalcolmnorwood.stupidchess.services.mongo_operations_service import MongoOperationsService
from com.johnmalcolmnorwood.stupidchess.services.move_application_service import MoveApplicationService
from com.johnmalcolmnorwood.stupidchess.models.game import Game
from com.johnmalcolmnorwood.stupidchess.models.move import Move


class StupidChessApplicationContext:
    def __init__(self):
        self.mongo_game_service = MongoOperationsService(Game, exclude_fields=['createTimestamp', 'lastUpdateTimestamp'])
        self.mongo_move_service = MongoOperationsService(Move)
        self.move_application_service = MoveApplicationService(self.mongo_game_service, self.mongo_move_service)
