import base64
import os

import aiohttp

from models.api import TokenGeneratorServiceRespModel
from models.exceptions import ServiceUnavailableException


async def generate_new_token(id, role):
    user, password = os.getenv("USER_BASIC"), os.getenv("PASSWORD_BASIC")
    if user is None or password is None:
        raise ValueError("User or password is missing")

    session = aiohttp.ClientSession()
    session.headers.setdefault('Content-Type', 'application/json')
    session.headers.setdefault('Authorization', base64.b64encode(f'{user}:{password}'.encode('utf-8')).decode('utf-8'))


    response = await session.post("http://token-generator-service:8080/jwt/generate_new", json={"id": id, "role": role})
    if response.status == 500:
        raise ServiceUnavailableException("cannot make request")

    access = await response.json()
    if access is None or len(access) == 0:
        raise ValueError("Access token is missing")

    return TokenGeneratorServiceRespModel(access_token=access['access_token'])