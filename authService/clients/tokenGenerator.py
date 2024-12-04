import base64
import os
from typing import Tuple

import aiohttp

from authService.models.api import TokenGeneratorServiceRespModel, TokenGeneratorVerifyToken
from authService.models.exceptions import ServiceUnavailableException, TokenVerifyException

_token_generator_urls = {
    "prod": {
        "verify": "http://token-generator-service:8080/jwt/verify",
        "generate_new": "http://token-generator-service:8080/jwt/generate_new"
    },
    "test": {
        "verify": "http://localhost:8085/jwt/verify",
        "generate_new": "http://localhost:8085/jwt/generate_new"
    }
}

async def get_token_generator_url(action: str) -> str:
    if action is None:
        raise ValueError("Action cannot be None")

    mode = os.getenv("SERVICE_MODE")
    if mode is not None:
        return _token_generator_urls[mode][action]
    raise ValueError("Mode cannot be None")



async def get_creds() -> Tuple[str, str]:
    user, password = os.getenv("USER_BASIC"), os.getenv("PASSWORD_BASIC")
    if user is None or password is None:
        raise ValueError("User or password is missing")

    return user, password

async def create_session_with_creds() -> aiohttp.ClientSession:
    user, password = await get_creds()

    session = aiohttp.ClientSession()
    session.headers.setdefault('Content-Type', 'application/json')
    session.headers.setdefault('Authorization', base64.b64encode(f'{user}:{password}'.encode('utf-8')).decode('utf-8'))

    return session

async def generate_new_token(id, role):
    session = await create_session_with_creds()
    response = await session.post(await get_token_generator_url("generate_new"), json={"id": id, "role": role})
    if response.status == 500:
        raise ServiceUnavailableException("cannot make request")

    access = await response.json()
    if access is None or len(access) == 0:
        raise ValueError("Access token is missing")

    return TokenGeneratorServiceRespModel(access_token=access['access_token'])

async def verify_token(token: str) -> TokenGeneratorVerifyToken:
    session = await create_session_with_creds()
    try:
        response = await session.post(await get_token_generator_url("verify"), json={"token": token})
    except ValueError as e:
        raise ValueError("Token verification failed", e)

    await session.close()
    if response.status == 500:
        raise ServiceUnavailableException("cannot make request")

    data = await response.json()
    if response.status == 400:
        raise TokenVerifyException(data)

    return TokenGeneratorVerifyToken(**data)