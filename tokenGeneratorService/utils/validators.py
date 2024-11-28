import base64
import os

from utils.exceptions import ValidationError


def required_str(v: str):
    assert len(v) > 0
    return v

def required_int(v: int):
    assert v > 0
    return v

def validate_authorization_header(content: str):
    content_string = base64.standard_b64decode(content.encode('utf-8'))
    content_string = content_string.decode('utf-8')

    splitted = content_string.split(":")
    if len(splitted) != 2:
        raise ValidationError("user or password cannot be empty")
    user = splitted[0]
    password = splitted[1]

    env_user, env_password = os.getenv("USER_BASIC"), os.getenv("PASSWORD_BASIC")
    if env_user is None or env_password is None:
        raise ValidationError("can't get user or password")

    if user != env_user or password != env_password:
        raise ValidationError("user or password is incorrect")

    return True