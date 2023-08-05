#!/usr/local/bin/python
import json
import os.path
from flask import Flask, jsonify
from .utils.application_context import ApplicationContext
from .utils.version import load_version_info

app = Flask(__name__)
app.context = ApplicationContext(app)

version_info = load_version_info(os.path.dirname(__file__))

@app.route("/server-version.json")
def server_version():
    return jsonify(version_info)
