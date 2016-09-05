#!/bin/python
from flask import Flask

app = Flask(__name__)

@app.route('/api/')
def hello_world():
    return 'Hello, World!'
