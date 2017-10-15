from wtforms import StringField, PasswordField, validators, ValidationError
from flask_wtf import FlaskForm
from wtforms.widgets import PasswordInput
from flask import current_app


def _get_render_kw(**kwargs):
    default = {
        "required": True,
        "value": False,
    }

    default.update(kwargs)
    return default


def _check_user_exists(_, field):
    username = field.data
    if current_app.context.user_service.get_user_with_username(username) is not None:
        raise ValidationError(f"User with name {username} already exists!")


# Hacky, but the stupid input field sets the value attribute on the generated html element and this doesn't play nice
# with the Material library I'm using
PasswordField.widget = PasswordInput(hide_value=False)

_USERNAME_REGEX = r"[a-zA-z0-9]*"
_PASSWORD_REGEX = r"[a-zA-z0-9!@#$%^&*]*"

_LOGIN_USERNAME_VALIDATORS = [
    validators.DataRequired(),
    validators.Length(min=4, max=16),
    validators.Regexp(_USERNAME_REGEX),
]

_CREATE_USERNAME_VALIDATORS = [
    *_LOGIN_USERNAME_VALIDATORS,
    _check_user_exists,
]

_LOGIN_PASSWORD_VALIDATORS = [
    validators.DataRequired(),
]

_CREATE_PASSWORD_VALIDATORS = [
    *_LOGIN_PASSWORD_VALIDATORS,
    validators.Length(min=8, max=32),
    validators.Regexp(_PASSWORD_REGEX),
]


class LoginForm(FlaskForm):
    username = StringField("Username", validators=_LOGIN_USERNAME_VALIDATORS, render_kw=_get_render_kw(placeholder="username"))
    password = PasswordField("Password", validators=_LOGIN_PASSWORD_VALIDATORS, render_kw=_get_render_kw(placeholder="password"))


class CreateAccountForm(FlaskForm):
    username = StringField("Username", validators=_CREATE_USERNAME_VALIDATORS, render_kw=_get_render_kw(placeholder="username"))
    password = PasswordField("Password", validators=_CREATE_PASSWORD_VALIDATORS, render_kw=_get_render_kw(placeholder="password"))
    confirm_password = PasswordField("Confirm Password", validators=[validators.EqualTo("password")], render_kw=_get_render_kw(placeholder="confirm password"))


class ChangePasswordForm(FlaskForm):
    password = PasswordField("Password", validators=_LOGIN_PASSWORD_VALIDATORS, render_kw=_get_render_kw(placeholder="password"))
    new_password = PasswordField("New Password", validators=_LOGIN_PASSWORD_VALIDATORS, render_kw=_get_render_kw(placeholder="new password"))
    confirm_new_password = PasswordField("Confirm New Password", validators=[validators.EqualTo("new_password")], render_kw=_get_render_kw(placeholder="confirm new password"))
