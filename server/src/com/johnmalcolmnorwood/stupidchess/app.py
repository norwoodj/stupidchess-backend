#!/usr/local/bin/python
from flask_mongoengine import MongoEngine
from flask import Flask
from com.johnmalcolmnorwood.stupidchess.blueprints.game_blueprint import game_blueprint
from com.johnmalcolmnorwood.stupidchess.utils.stupid_chess_application_context import StupidChessApplicationContext


app = Flask(__name__)
app.register_blueprint(game_blueprint, url_prefix='/api/game')
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongo',
    'db': 'stupidchess'
}

app.cxt = StupidChessApplicationContext()

db = MongoEngine(app)
