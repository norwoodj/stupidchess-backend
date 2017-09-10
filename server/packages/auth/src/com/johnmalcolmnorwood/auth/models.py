#!/usr/local/bin/python


class User:
    @property
    def is_authenticated(self):
        raise NotImplementedError()

    @property
    def is_active(self):
        raise NotImplementedError()

    @property
    def is_anonymous(self):
        raise NotImplementedError()

    @property
    def username(self):
        raise NotImplementedError()

    def get_id(self):
        raise NotImplementedError()
