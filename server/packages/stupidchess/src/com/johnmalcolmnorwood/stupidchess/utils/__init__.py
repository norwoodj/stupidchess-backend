#!/usr/local/bin/python
from uuid import uuid4
import base64

UUID_REGEX = "[A-Z2-7]{26}"


def random_uuid():
    return base64.b32encode(uuid4().bytes).decode("utf-8").rstrip("=")


def to_title_case(input):
    return " ".join(s[0].upper() + s[1:].lower() for s in input.split("_"))
