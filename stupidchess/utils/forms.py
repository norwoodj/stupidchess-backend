from flask_wtf import FlaskForm
from flask import current_app
from wtforms import StringField, validators, ValidationError, SelectField
from ..models.game import GameType, GameAuthType
from . import to_title_case


def _get_render_kw(**kwargs):
    default = {
        "required": True,
        "value": False,
    }

    default.update(kwargs)
    return default


def _check_user_exists(form, field):
    username = field.data

    if form.num_players.data == GameAuthType.ONE_PLAYER:
        return

    if current_app.context.user_service.get_user_with_username(username) is None:
        raise ValidationError(f"User with name {username} does not exist!")


_OTHER_PLAYER_NAME_VALIDATORS = [
    validators.DataRequired(),
    _check_user_exists,
]


def _to_choices(enum_values):
    return [(e, to_title_case(e)) for e in enum_values]


class CreateGameForm(FlaskForm):
    game_type = SelectField("Game Type", choices=_to_choices(GameType.all()))
    num_players = SelectField(
        "Number of Players", choices=_to_choices(GameAuthType.all())
    )
    other_player = StringField(
        "Other Player Name",
        validators=_OTHER_PLAYER_NAME_VALIDATORS,
        render_kw=_get_render_kw(placeholder="other player name"),
    )
