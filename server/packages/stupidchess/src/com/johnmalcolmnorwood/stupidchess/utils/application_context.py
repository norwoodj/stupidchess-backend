#!/usr/local/bin/python
import logging
import os
from flask_mongoengine import MongoEngine
from mongoengine.connection import get_db
from healthcheck import HealthCheck
from jconfigure import configure

from com.johnmalcolmnorwood.stupidchess.services.ambiguous_move_service import AmbiguousMoveService
from com.johnmalcolmnorwood.stupidchess.services.move_application_service import MoveApplicationService
from com.johnmalcolmnorwood.stupidchess.services.move_move_update_service import MoveMoveUpdateService
from com.johnmalcolmnorwood.stupidchess.services.place_move_update_service import PlaceMoveUpdateService
from com.johnmalcolmnorwood.stupidchess.services.possible_move_service import PossibleMoveService
from com.johnmalcolmnorwood.stupidchess.services.sc_user_service import ScUserService
from com.johnmalcolmnorwood.stupidchess.utils.game_rules import SETUP_SQUARES_FOR_COLOR, BOARD_SQUARES_FOR_GAME_TYPE
from com.johnmalcolmnorwood.stupidchess.utils.game_rules import BOARD_MIDDLE_SECTION_FOR_GAME_TYPE

_LOGGER = logging.getLogger(__name__)


class ApplicationContext:
    def __init__(self, app):
        self.config = configure()
        _LOGGER.debug(self.config)

        self.__initialize_app(app)
        self.__initialize_mongo(app)
        self.__initialize_healthcheck(app)

        self.possible_move_service = PossibleMoveService(
            BOARD_SQUARES_FOR_GAME_TYPE,
            BOARD_MIDDLE_SECTION_FOR_GAME_TYPE,
        )

        self.move_update_services = (
            PlaceMoveUpdateService(SETUP_SQUARES_FOR_COLOR),
            MoveMoveUpdateService(self.possible_move_service),
        )

        self.move_application_service = MoveApplicationService(self.move_update_services)
        self.ambiguous_move_service = AmbiguousMoveService()

        self.user_service = ScUserService()

    def __initialize_app(self, app):
        app.config.update(self.config)
        app.secret_key = self.config["app_secret_key"]

    def __initialize_mongo(self, app):
        MongoEngine(app)

    def __initialize_healthcheck(self, app):
        _LOGGER.debug("Setting up healthcheck endpoint at {}".format(self.config["healthcheck_endpoint"]))
        health = HealthCheck(app, self.config["healthcheck_endpoint"])

        def mongo_okay():
            db = get_db()
            stats = db.command("dbstats")
            return bool(stats["ok"]), "Mongo Database is UP" if stats["ok"] else "ERROR: Mongo Database is DOWN"

        health.add_check(mongo_okay)
