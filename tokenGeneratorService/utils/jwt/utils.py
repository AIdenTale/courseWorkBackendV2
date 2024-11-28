import datetime
import os

import jwt

from tokenGeneratorService.utils.jwt.exceptions import JWTErrGetSecret

JWT_SECRET_ENV = "JWT_SECRET"


def gen_jwt_with_claims(user_id: int, role: str):
    jwt_secret = os.getenv(JWT_SECRET_ENV)
    if len(jwt_secret) == 0:
        raise JWTErrGetSecret("failed get jwt secret")

    encoded_jwt = jwt.encode(
        {
            "id": user_id,
            "role": role,
            "iat": datetime.datetime.now(tz=datetime.timezone.utc),
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1),
        },
        jwt_secret,
        algorithm="HS256"
    )

    return encoded_jwt

def jwt_verify_token(token):
    jwt_secret = os.getenv(JWT_SECRET_ENV)
    if len(jwt_secret) == 0:
        raise JWTErrGetSecret("failed get jwt secret")

    decode_payload = jwt.decode(
        token,
        jwt_secret,
        options={
            "verify_exp": True,
            "verify_signature": True,
        },
        algorithms=["HS256"]
    )

    return decode_payload