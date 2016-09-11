#!/usr/local/bin/python
from com.johnmalcolmnorwood.stupidchess.services.possible_move_service import PossibleMoveService
from com.johnmalcolmnorwood.stupidchess.services.move_application_service import MoveApplicationService
from com.johnmalcolmnorwood.stupidchess.utils import SETUP_SQUARES_FOR_COLOR, BOARD_SQUARES_FOR_GAME_TYPE
from com.johnmalcolmnorwood.stupidchess.utils import BOARD_MIDDLE_SECTION_FOR_GAME_TYPE


class ApplicationContext:
    def __init__(self):
        self.possible_move_service = PossibleMoveService(
            BOARD_SQUARES_FOR_GAME_TYPE,
            BOARD_MIDDLE_SECTION_FOR_GAME_TYPE
        )

        self.move_application_service = MoveApplicationService(SETUP_SQUARES_FOR_COLOR, self.possible_move_service)
