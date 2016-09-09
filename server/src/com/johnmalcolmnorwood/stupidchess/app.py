#!/usr/local/bin/python
from com.johnmalcolmnorwood.stupidchess.blueprints.game_blueprint import game_blueprint
from com.johnmalcolmnorwood.stupidchess.utils.application_context import ApplicationContext
from flask import Flask
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.register_blueprint(game_blueprint, url_prefix='/api/game')
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongo',
    'db': 'stupidchess'
}

app.context = ApplicationContext()

MongoEngine(app)
