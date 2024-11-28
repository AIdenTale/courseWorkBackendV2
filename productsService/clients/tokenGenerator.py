import base64
import os

import aiohttp

from productsService.models.exception import ServiceUnavailableException, TokenVerifyException


async def verify_token(token: str):
    user, password = os.getenv("USER_BASIC"), os.getenv("PASSWORD_BASIC")
    if user is None or password is None:
        raise ValueError("User or password is missing")

    session = aiohttp.ClientSession()
    session.headers.setdefault('Content-Type', 'application/json')
    session.headers.setdefault('Authorization', base64.b64encode(f'{user}:{password}'.encode('utf-8')).decode('utf-8'))


    response = await session.post("http://token-generator-service:8080/jwt/verify", json={"token": token})
    if response.status == 500:
        raise ServiceUnavailableException("cannot make request")

    if response.status == 400:
        data = await response.json()
        raise TokenVerifyException(data)

    return True