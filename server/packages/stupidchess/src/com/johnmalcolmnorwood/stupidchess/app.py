#!/usr/local/bin/python
from flask import Flask, jsonify
from .utils.application_context import ApplicationContext

app = Flask(__name__)
app.context = ApplicationContext(app)
