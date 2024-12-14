from authService.clients.db import add_new_user, get_user_by_login_and_password, get_user_by_id
from authService.clients.tokenGenerator import generate_new_token

from authService.models.api import Error, \
    User, Error, LoginSuccessResponse, UserLoginRequest, TokenGeneratorTokenGenRequest
from authService.models.exceptions import ServiceUnavailableException, EmailAlreadyRegistered
from authService.utils.utils import get_hash_password


async def register_user(user: UserLoginRequest):
        hash_password = get_hash_password(user.password)
        user.password = hash_password

        try:
            id, role = add_new_user(user)
        except EmailAlreadyRegistered as e:
            return e

        try:
            data = await generate_new_token(id, role)
            return LoginSuccessResponse(access_token=data.access_token)

        except ServiceUnavailableException as jwtException:
            print(f"ERROR WHILE GENERATING JWT: {jwtException}")
            return Error(message="JWT generation failed, pls contact admins: admin@admin.ru")

        except Exception as exception:
            print(f"UNEXPECTED ERROR: {exception}")
            return Error(message="JWT generation failed, pls contact admins: admin@admin.ru")

async def auth_user(user: UserLoginRequest):
        hash_password = get_hash_password(user.password)
        user.password = hash_password

        payload = get_user_by_login_and_password(user)

        if payload is None:
            return Error(message="user not found")

        id, role = payload[0], payload[1]

        try:
            data = await generate_new_token(id, role)
            return LoginSuccessResponse(access_token=data.access_token)

        except ServiceUnavailableException as jwtException:
            print(f"ERROR WHILE GENERATING JWT: {jwtException}")
            return Error(message="JWT generation failed, pls contact admins: admin@admin.ru")

        except Exception as exception:
            print(f"UNEXPECTED ERROR: {exception}")
            return Error(message="JWT generation failed, pls contact admins: admin@admin.ru")

async def get_user_profile(userTokenInfo: TokenGeneratorTokenGenRequest):
        userInfoRecords = get_user_by_id(userTokenInfo.id)
        if userInfoRecords is None:
            return Error(message="User not found")

        return User(email=userInfoRecords[0],name=userInfoRecords[1], surname=userInfoRecords[2], role=userInfoRecords[3])





