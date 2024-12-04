import os

from fastapi import Request
from starlette.responses import JSONResponse

from authService.clients.tokenGenerator import verify_token
from authService.models.api import TokenGeneratorVerifyToken
from authService.models.exceptions import ServiceUnavailableException, TokenVerifyException

JWT_TOKEN_TYPE = "Bearer"

async def verify_token_middleware(request: Request) -> TokenGeneratorVerifyToken | JSONResponse:
    # mode = os.getenv("SERVICE_MODE")
    # if mode is not None:
    #     if mode == "test":
    #         return TokenGeneratorVerifyToken(id=1, role="admin")
    #     else:
    #         pass

    authorization = request.headers.get('Authorization')
    if authorization is None:
        return JSONResponse({"error": "unauthorized", "message": "cannot get token"},status_code=401)

    payload = authorization.split(" ")
    if len(payload) != 2:
        return JSONResponse({"error": "unauthorized", "message": "cannot get token"}, status_code=401)

    if payload[0] != JWT_TOKEN_TYPE:
        return JSONResponse({"error": "unauthorized", "message": "invalid token type"}, status_code=401)

    try:
        return await verify_token(payload[1])
    except ServiceUnavailableException as e:
        return JSONResponse({"error": "internal service error"}, status_code=500)

    except TokenVerifyException as e:
        return JSONResponse({"error": "unauthorized", "message": e.message}, status_code=401)

    except ValueError as e:
        print("VERIFY TOKEN ERROR: "+str(e))
        return JSONResponse({"error": "internal service error"}, status_code=500)
    except Exception as e:
        print("VERIFY TOKEN ERROR: " + str(e))
        return JSONResponse({"error": "internal service error"}, status_code=500)

