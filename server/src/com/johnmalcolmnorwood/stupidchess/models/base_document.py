#!/usr/local/bin/python
from flask_mongoengine import Document
from mongoengine import StringField, DateTimeField
from datetime import datetime
from uuid import uuid4


class BaseDocument(Document):
    _id = StringField(required=True, default=lambda: str(uuid4()))
    createTimestamp = DateTimeField(required=True, default=datetime.utcnow)
    lastUpdateTimestamp = DateTimeField(required=True, default=datetime.utcnow)

    meta = {'allow_inheritance': True}
