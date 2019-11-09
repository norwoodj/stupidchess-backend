#!/usr/local/bin/python
import bcrypt
from flask_auth_utils import user_service
from ..models.user import User


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


class UserService(user_service.UserService):
    def __init__(self, user_dao):
        self.__user_dao = user_dao

    def get_user_with_id(self, id):
        user = self.__user_dao.find_one_or_none({"_id": id})
        return AuthUser(user) if user is not None else None

    def get_user_with_username(self, username):
        user = self.__user_dao.find_one_or_none({"username": username})
        return AuthUser(user) if user is not None else None

    def get_user_with_credentials(self, username, password):
        user = self.__user_dao.find_one_or_none({"username": username})

        if user is not None and bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
            return AuthUser(user)

    def create_user(self, username, password):
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        user = User(
            username=username,
            password=hashed_password,
        )

        self.__user_dao.insert(user)
        return AuthUser(user)

    def update_user_password(self, username, password):
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        self.__user_dao.update_matching(
            {"username": username},
            {"$set": {"password": hashed_password}, "$currentDate": {"lastUpdateTimestamp": True}}
        )
