#!/usr/local/bin/python
from com.johnmalcolmnorwood.stupidchess.services.ambiguous_move_service import AmbiguousMoveService
from com.johnmalcolmnorwood.stupidchess.services.move_application_service import MoveApplicationService
from com.johnmalcolmnorwood.stupidchess.services.move_move_update_service import MoveMoveUpdateService
from com.johnmalcolmnorwood.stupidchess.services.place_move_update_service import PlaceMoveUpdateService
from com.johnmalcolmnorwood.stupidchess.services.possible_move_service import PossibleMoveService
from com.johnmalcolmnorwood.stupidchess.utils.game_rules import SETUP_SQUARES_FOR_COLOR, BOARD_SQUARES_FOR_GAME_TYPE
from com.johnmalcolmnorwood.stupidchess.utils.game_rules import BOARD_MIDDLE_SECTION_FOR_GAME_TYPE


class ApplicationContext:
    def __init__(self):
        self.possible_move_service = PossibleMoveService(
            BOARD_SQUARES_FOR_GAME_TYPE,
            BOARD_MIDDLE_SECTION_FOR_GAME_TYPE
        )

        self.move_update_services = (
            PlaceMoveUpdateService(SETUP_SQUARES_FOR_COLOR),
            MoveMoveUpdateService(self.possible_move_service),
        )

        self.move_application_service = MoveApplicationService(self.move_update_services)
        self.ambiguous_move_service = AmbiguousMoveService()
