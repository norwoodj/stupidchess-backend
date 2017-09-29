#!/usr/local/bin/python
import bcrypt
from mongoengine import DoesNotExist

from com.johnmalcolmnorwood.auth.user_service import UserService, UserAlreadyExistsException
from com.johnmalcolmnorwood.stupidchess.models.user import User


class AuthUser:
    def __init__(self, user):
        self.__user = user

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def id(self):
        return self.get_id()

    @property
    def username(self):
        return self.__user.username

    def get_id(self):
        return self.__user.get_id()


class ScUserService(UserService):
    @staticmethod
    def __get_user_safe(**kwargs):
        try:
            return User.objects.get(**kwargs)
        except DoesNotExist:
            return None

    def get_user_with_id(self, id):
        user = ScUserService.__get_user_safe(_id=id)
        return AuthUser(user) if user is not None else None

    def get_user_with_username(self, username):
        user = ScUserService.__get_user_safe(username=username)
        return AuthUser(user) if user is not None else None

    def get_user_with_credentials(self, username, password):
        user = ScUserService.__get_user_safe(username=username)

        if user is not None and bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
            return AuthUser(user)

    def create_user(self, username, password, *args, **kwargs):
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        user = User(
            username=username,
            password=hashed_password,
        )

        user.save()
        return AuthUser(user)

    def update_user_password(self, username, password):
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        User.objects(username=username).update(__raw__={
            "$set": {"password": hashed_password},
            "$currentDate": {"lastUpdateTimestamp": True},
        })
