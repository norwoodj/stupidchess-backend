#!/usr/local/bin/python


class UserService:
    def get_user_with_id(self, id):
        raise NotImplementedError()

    def get_user_with_credentials(self, username, password):
        raise NotImplementedError()

    def create_user(self, username, password, *args, **kwargs):
        raise NotImplementedError()
