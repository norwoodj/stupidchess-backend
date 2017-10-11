#!/usr/local/bin/python
from flask import Blueprint, render_template, request, current_app, redirect, url_for
from flask_login import current_user
from flask.ext.login import login_required
from ..utils.forms import CreateGameForm


template_blueprint = Blueprint("template", __name__)


@template_blueprint.route("/")
def index():
    return render_template("index.html", current_user=current_user)


@template_blueprint.route("/profile")
@login_required
def profile():
    if "userUuid" not in request.args:
        return render_template(
            "profile.html",
            current_user=current_user,
            profile_user_uuid=current_user.get_id(),
            profile_user_name=current_user.username,
        )

    other_user_uuid = request.args["userUuid"]
    other_user = current_app.context.user_service.get_user_with_id(other_user_uuid)

    if other_user is None:
        return render_template(
            "profile.html",
            current_user=current_user,
            profile_user_uuid=current_user.get_id(),
            profile_user_name=current_user.username,
            error=f"User with ID {other_user_uuid} does not exist!",
        )

    return render_template(
        "profile.html",
        current_user=current_user,
        profile_user_uuid=other_user.get_id(),
        profile_user_name=other_user.username,
    )


@template_blueprint.route("/game")
@login_required
def game():
    if "gameUuid" not in request.args:
        return render_template(
            "game.html",
            current_user=current_user,
            error=f"Must provide 'gameUuid' query parameter when requesting game page!",
        ), 400

    game_uuid = request.args["gameUuid"]

    if not current_app.context.game_service.game_with_uuid_for_user_exists(game_uuid, current_user.get_id()):
        return render_template(
            "game.html",
            current_user=current_user,
            error=f"No Game with ID {game_uuid} exists!",
        ), 400

    return render_template("game.html", game_uuid=game_uuid, current_user=current_user)


@template_blueprint.route("/create-game", methods=["GET", "POST"])
@login_required
def create_game():
    form = CreateGameForm(request.form)

    if request.method == "POST" and form.validate():
        game = current_app.context.game_service.create_game(
            game_type=form.game_type.data,
            game_auth_type=form.num_players.data,
            other_player=form.other_player.data,
        )

        return redirect(url_for("template.game", gameUuid=game.get_id()))

    return render_template("create-game.html", form=form, current_user=current_user)
