from mongoengine import StringField
from .base_document import BaseDocument


class User(BaseDocument):
    meta = {
        "indexes": [{
            "fields": ["username"],
            "unique": True,
        }],
    }

    username = StringField(required=True)
    password = StringField(required=True)
