#!/usr/local/bin/python
from flask_mongoengine import Document
from mongoengine import StringField, DateTimeField
from datetime import datetime
from uuid import uuid4
from com.johnmalcolmnorwood.stupidchess.models import UUID_REGEX


class BaseDocument(Document):
    _id = StringField(required=True, regex=UUID_REGEX, default=lambda: str(uuid4()))
    createTimestamp = DateTimeField(required=True, default=datetime.utcnow)
    lastUpdateTimestamp = DateTimeField(required=True, default=datetime.utcnow)

    def get_id(self):
        return self._id

    meta = {'abstract': True}
