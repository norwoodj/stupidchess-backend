#!/usr/local/bin/python
from flask import Blueprint, request, current_app, render_template, redirect, url_for, jsonify
from flask_login import login_user, current_user, login_required, logout_user, fresh_login_required
from . import LOGGER
from .forms import ChangePasswordForm, CreateAccountForm, LoginForm
from .utils import redirect_to_next

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)

    if request.method == "POST" and form.validate():
        user = current_app.context.user_service.get_user_with_credentials(form.username.data, form.password.data)

        if user is not None:
            login_user(user, remember=True)
            return redirect_to_next(current_app.config["auth"]["postLoginRedirect"])

        form.password.errors.append("Invalid username or password provided in login request!")

    return render_template(
        current_app.config["auth"]["loginTemplate"],
        form=form,
        current_user=current_user,
    ), 200 if request.method == "GET" else 400


@auth_blueprint.route("/logout")
@login_required
def logout():
    LOGGER.debug(f"Successfully logged out user '{current_user.username}'")
    logout_user()
    return redirect(url_for(current_app.config["auth"]["postLogoutRedirect"]))


@auth_blueprint.route("/create-account", methods=["GET", "POST"])
def create_account():
    form = CreateAccountForm(request.form)

    if request.method == "POST" and form.validate():
        user = current_app.context.user_service.create_user(form.username.data, form.password.data)
        login_user(user, remember=True)
        return redirect(url_for(current_app.config["auth"]["postLoginRedirect"]))

    return render_template(
        current_app.config["auth"]["createAccountTemplate"],
        form=form,
        current_user=current_user,
    ), 200 if request.method == "GET" else 400


@auth_blueprint.route("/change-password", methods=["GET", "POST"])
@fresh_login_required
def change_password():
    form = ChangePasswordForm(request.form)

    if request.method == "POST" and form.validate():
        user = current_app.context.user_service.get_user_with_credentials(current_user.username, form.password.data)

        if user is not None:
            current_app.context.user_service.update_user_password(current_user.username, form.new_password.data)
            return redirect(url_for(current_app.config["auth"]["postLoginRedirect"]))

        form.password.errors.append("Invalid current password provided in request!")

    return render_template(
        current_app.config["auth"]["changePasswordTemplate"],
        form=form,
        current_user=current_user,
    ), 200 if request.method == "GET" else 400
