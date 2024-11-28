from authService.clients.db import PostgresClient
from authService.clients.tokenGenerator import generate_new_token

from authService.models.api import UserAuthReqModel, ErrorRespModel, UserAuthRespModel, UserNotFound, UserLoginReqModel
from authService.models.exceptions import ServiceUnavailableException, EmailAlreadyRegistered
from authService.utils.utils import get_hash_password



class AuthService:
    async def register_user(self, user: UserAuthReqModel):
        client = PostgresClient()

        hash_password = get_hash_password(user.password)
        user.password = hash_password

        try:
            id, role = client.add_new_user(user)
        except EmailAlreadyRegistered as e:
            return e

        try:
            data = await generate_new_token(id, role)
            return UserAuthRespModel(access_token=data.access_token)

        except ServiceUnavailableException as jwtException:
            print(f"ERROR WHILE GENERATING JWT: {jwtException}")
            return ErrorRespModel(message="JWT generation failed, pls contact admins: admin@admin.ru")

        except Exception as exception:
            print(f"UNEXPECTED ERROR: {exception}")
            return ErrorRespModel(message="JWT generation failed, pls contact admins: admin@admin.ru")

    async def auth_user(self, user: UserLoginReqModel):
        client = PostgresClient()

        hash_password = get_hash_password(user.password)
        user.password = hash_password

        payload = client.get_user(user)

        if payload is None:
            return UserNotFound(message="User not found")

        id, role = payload[0], payload[1]

        try:
            data = await generate_new_token(id, role)
            return UserAuthRespModel(access_token=data.access_token)

        except ServiceUnavailableException as jwtException:
            print(f"ERROR WHILE GENERATING JWT: {jwtException}")
            return ErrorRespModel(message="JWT generation failed, pls contact admins: admin@admin.ru")

        except Exception as exception:
            print(f"UNEXPECTED ERROR: {exception}")
            return ErrorRespModel(message="JWT generation failed, pls contact admins: admin@admin.ru")





