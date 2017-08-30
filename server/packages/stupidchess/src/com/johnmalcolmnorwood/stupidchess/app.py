#!/usr/local/bin/python
from flask import Flask, jsonify
from com.johnmalcolmnorwood.stupidchess.blueprints.game_blueprint import game_blueprint
from com.johnmalcolmnorwood.stupidchess.exceptions import IllegalMoveException, InvalidGameParameterException
from com.johnmalcolmnorwood.stupidchess.utils.application_context import ApplicationContext
from com.johnmalcolmnorwood.auth.initialize_authentication import initialize_authentication

app = Flask(__name__)
app.context = ApplicationContext(app)

initialize_authentication(app, auth_url_prefix="/api/user")
app.register_blueprint(game_blueprint, url_prefix="/api/game")


@app.errorhandler(IllegalMoveException)
def handle_invalid_usage(error):
    return jsonify(
        message="Failed to apply illegal move",
        move=error.move.to_dict("startSquare", "destinationSquare", "type"),
    ), 400


@app.errorhandler(InvalidGameParameterException)
def handle_invalid_usage(error):
    return jsonify(message=error.message), 400
