#!/usr/local/bin/python
from flask import Blueprint, render_template


template_blueprint = Blueprint("template", __name__)


@template_blueprint.route("/profile", methods=["GET"])
def get_profile_page():
    return render_template("profile.html")
