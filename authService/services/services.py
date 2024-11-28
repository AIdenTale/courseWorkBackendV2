from authService.clients.db import PostgresClient
from authService.clients.tokenGenerator import generate_new_token

from authService.models.api import UserAuthReqModel, ErrorRespModel, UserAuthRespModel
from authService.models.exceptions import ServiceUnavailableException
from authService.utils.utils import get_hash_password

class AuthService:
    async def register_user(self, user: UserAuthReqModel):
        client = PostgresClient()

        hash_password = get_hash_password(user.password)
        user.password = hash_password

        id, role = client.add_new_user(user)

        try:
            data = await generate_new_token(id, role)
            return UserAuthRespModel(access_token=data.access_token)

        except ServiceUnavailableException as jwtException:
            print(f"ERROR WHILE GENERATING JWT: {jwtException}")
            return ErrorRespModel(message="JWT generation failed, pls contact admins: admin@admin.ru")

        except Exception as exception:
            print(f"UNEXPECTED ERROR: {exception}")
            return ErrorRespModel(message="JWT generation failed, pls contact admins: admin@admin.ru")





