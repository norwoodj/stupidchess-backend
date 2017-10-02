#!/usr/local/bin/python
from datetime import timedelta
from flask import jsonify
from flask_login import current_user
from flask_mongoengine import MongoEngine
from flask_wtf import CSRFProtect
from healthcheck import HealthCheck
from jconfigure import configure
from mongoengine.connection import get_db

from ...auth.initialize_authentication import initialize_authentication

from .. import LOGGER
from ..blueprints.game_blueprint import game_blueprint, post_move_to_game
from ..blueprints.record_blueprint import record_blueprint
from ..blueprints.template_blueprint import template_blueprint
from ..exceptions import InvalidMoveException, InvalidGameParameterException, ForbiddenMoveException
from ..services.ambiguous_move_service import AmbiguousMoveService
from ..services.move_application_service import MoveApplicationService
from ..services.move_move_update_service import MoveMoveUpdateService
from ..services.place_move_update_service import PlaceMoveUpdateService
from ..services.possible_move_service import PossibleMoveService
from ..services.sc_user_service import ScUserService
from ..services.game_service import GameService
from ..services.record_service import RecordService

from .game_rules import SETUP_SQUARES_FOR_COLOR, BOARD_SQUARES_FOR_GAME_TYPE
from .game_rules import BOARD_MIDDLE_SECTION_FOR_GAME_TYPE


class ApplicationContext:
    BLUEPRINTS = [
        ("game", game_blueprint),
        ("record", record_blueprint),
        ("template", template_blueprint),
    ]

    def __init__(self, app):
        self.config = configure()
        LOGGER.debug(self.config)

        self.__initialize_app(app)
        self.__initialize_csrf(app)
        self.__initialize_healthcheck(app)
        self.__initialize_mongo(app)
        self.__initialize_services()
        self.__initialize_auth(app)
        self.__register_blueprints(app)
        self.__register_error_handlers(app)

    def __initialize_app(self, app):
        self.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=self.config.get('remember_cookie_duration_days', 365))
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

    def __initialize_csrf(self, app):
        self.csrf = CSRFProtect(app)
        self.csrf.exempt(post_move_to_game)

    def __initialize_mongo(self, app):
        MongoEngine(app)

    def __initialize_services(self):
        self.ambiguous_move_service = AmbiguousMoveService()
        self.user_service = ScUserService()

        self.possible_move_service = PossibleMoveService(
            BOARD_SQUARES_FOR_GAME_TYPE,
            BOARD_MIDDLE_SECTION_FOR_GAME_TYPE,
        )

        self.move_update_services = (
            PlaceMoveUpdateService(SETUP_SQUARES_FOR_COLOR),
            MoveMoveUpdateService(self.possible_move_service),
        )

        self.move_application_service = MoveApplicationService(self.move_update_services)
        self.game_service = GameService(self.possible_move_service, self.move_application_service)
        self.record_service = RecordService(self.game_service)


    def __initialize_auth(self, app):
        initialize_authentication(
            app=app,
            user_service=self.user_service,
            auth_secret_key=self.config["app_secret_key"],
            auth_blueprint_prefix=self.config["endpoint_prefixes"].get("auth", ""),
            login_view="/login",
        )

    def __register_blueprints(self, app):
        for name, blueprint in ApplicationContext.BLUEPRINTS:
            LOGGER.debug(f"Registering {name} blueprint with prefix '{self.config['endpoint_prefixes'][name]}'")
            app.register_blueprint(blueprint, url_prefix=self.config["endpoint_prefixes"][name])

    def __register_error_handlers(self, app):
        @app.errorhandler(InvalidMoveException)
        def handle_invalid_move_error(error):
            return jsonify(
                message=f"Failed to apply invalid move",
                reason=error.reason,
                move=error.move.to_dict("startSquare", "destinationSquare", "type"),
            ), 400

        @app.errorhandler(InvalidGameParameterException)
        def handle_invalid_game_parameter_error(error):
            return jsonify(message=error.message), 400

        @app.errorhandler(ForbiddenMoveException)
        def handle_forbidden_move_error(error):
            return jsonify(
                message=f"User '{current_user.username}' is not authorized to perform this move",
                move=error.move.to_dict("startSquare", "destinationSquare", "type"),
            ), 403
