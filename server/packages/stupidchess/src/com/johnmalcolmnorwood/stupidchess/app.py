#!/usr/local/bin/python
from flask import Flask
from .utils.application_context import ApplicationContext

app = Flask(__name__)
app.context = ApplicationContext(app)
