#!/usr/local/bin/python
from flask_mongoengine import Document
from mongoengine import StringField, DateTimeField
from datetime import datetime

from ..utils import UUID_REGEX, random_uuid


class BaseDocument(Document):
    _id = StringField(required=True, regex=UUID_REGEX, default=random_uuid)
    createTimestamp = DateTimeField(required=True, default=datetime.utcnow)
    lastUpdateTimestamp = DateTimeField(required=True, default=datetime.utcnow)

    def get_id(self):
        return self._id

    meta = {'abstract': True}
