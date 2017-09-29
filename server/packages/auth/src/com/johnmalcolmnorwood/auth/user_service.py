#!/usr/local/bin/python


class UserAlreadyExistsException(Exception):
    def __init__(self, username):
        self.username = username


class UserService:
    def get_user_with_id(self, id):
        raise NotImplementedError()

    def get_user_with_username(self, username):
        raise NotImplementedError()

    def get_user_with_credentials(self, username, password):
        raise NotImplementedError()

    def create_user(self, username, password, *args, **kwargs):
        raise NotImplementedError()

    def update_user_password(self, username, password):
        raise NotImplementedError()
