#!/usr/local/bin/python
from uuid import uuid4
import base64

UUID_REGEX = "[A-Z2-7]{26}"


def random_uuid():
    return base64.b32encode(str(uuid4()).replace("-", "")[16:].encode()).decode("utf-8").rstrip("=")

