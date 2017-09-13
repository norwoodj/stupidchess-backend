#!/usr/local/bin/python
import logging
import os

from flask import jsonify
from flask_mongoengine import MongoEngine
from healthcheck import HealthCheck
from jconfigure import configure
from mongoengine.connection import get_db

from ...auth.initialize_authentication import initialize_authentication

from .. import LOGGER
from ..blueprints.game_blueprint import game_blueprint
from ..exceptions import IllegalMoveException, InvalidGameParameterException
from ..services.ambiguous_move_service import AmbiguousMoveService
from ..services.move_application_service import MoveApplicationService
from ..services.move_move_update_service import MoveMoveUpdateService
from ..services.place_move_update_service import PlaceMoveUpdateService
from ..services.possible_move_service import PossibleMoveService
from ..services.sc_user_service import ScUserService

from .game_rules import SETUP_SQUARES_FOR_COLOR, BOARD_SQUARES_FOR_GAME_TYPE
from .game_rules import BOARD_MIDDLE_SECTION_FOR_GAME_TYPE


class ApplicationContext:
    def __init__(self, app):
        self.config = configure()
        LOGGER.debug(self.config)

        self.__initialize_app(app)
        self.__initialize_healthcheck(app)
        self.__initialize_mongo(app)
        self.__initialize_services()
        self.__initialize_auth(app)
        self.__register_blueprints(app)
        self.__register_error_handlers(app)

    def __initialize_app(self, app):
        app.config.update(self.config)

    def __initialize_healthcheck(self, app):
        healthcheck_endpoint = self.config["endpoint_prefixes"]["healthcheck"]
        LOGGER.debug(f"Setting up healthcheck endpoint at {healthcheck_endpoint}")
        health = HealthCheck(app, healthcheck_endpoint)

        def mongo_okay():
            db = get_db()
            stats = db.command("dbstats")
            return bool(stats["ok"]), "Mongo Database is UP" if stats["ok"] else "ERROR: Mongo Database is DOWN"

        health.add_check(mongo_okay)

    def __initialize_mongo(self, app):
        MongoEngine(app)

    def __initialize_services(self):
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

    def __initialize_auth(self, app):
        initialize_authentication(
            app=app,
            user_service=self.user_service,
            auth_secret_key=self.config["app_secret_key"],
            auth_blueprint_prefix=self.config["endpoint_prefixes"].get("auth", ""),
        )

    def __register_blueprints(self, app):
        LOGGER.debug(f"Registering game blueprint with prefix {self.config['endpoint_prefixes']['game']}")
        app.register_blueprint(game_blueprint, url_prefix=self.config["endpoint_prefixes"]["game"])

    def __register_error_handlers(self, app):
        @app.errorhandler(IllegalMoveException)
        def handle_invalid_usage(error):
            return jsonify(
                message="Failed to apply illegal move",
                move=error.move.to_dict("startSquare", "destinationSquare", "type"),
            ), 400

        @app.errorhandler(InvalidGameParameterException)
        def handle_invalid_usage(error):
            return jsonify(message=error.message), 400
