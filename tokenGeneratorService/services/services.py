import jwt

from tokenGeneratorService.models.api import UserAuthRespModel, ErrorRespModel, VerifyTokenRespModel
from tokenGeneratorService.utils.jwt.exceptions import JWTErrGetSecret
from tokenGeneratorService.utils.jwt.utils import gen_jwt_with_claims, jwt_verify_token


async def generate_new_token(user_id: int, role: str):
    try:
        token = gen_jwt_with_claims(user_id, role)
        return UserAuthRespModel(access_token=token)
    except JWTErrGetSecret as jwtError:
        print(f"JWT GEN ERROR: {jwtError}")
        return ErrorRespModel(message="jwt gen error")
    except Exception as e:
        print(f"unexpected error: {e}")
        return ErrorRespModel(message="internal server error")

async def verify_token(token: str):
    try:
        decode_payload = jwt_verify_token(token)
        return VerifyTokenRespModel(id=decode_payload["id"], role=decode_payload["role"])
    except JWTErrGetSecret as jwtError:
        print(f"JWT VERIFY ERROR: {jwtError}")
        return ErrorRespModel(message="jwt gen error")
    except jwt.ExpiredSignatureError:
        return ErrorRespModel(message="token is expired")
    except jwt.InvalidSignatureError:
        return ErrorRespModel(message="token is invalid")
    except Exception as e:
        print(f"unexpected error: {e}")
        return ErrorRespModel(message="internal server error")

