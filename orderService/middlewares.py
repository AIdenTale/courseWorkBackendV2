import os

from fastapi import Request
from starlette.responses import JSONResponse

from orderService.clients.tokenGenerator import verify_token
from orderService.model.tokenGenerator import ServiceUnavailableException, TokenVerifyException, TokenGeneratorTokenGenRequest

JWT_TOKEN_TYPE = "Bearer"
BASIC_TOKEN_TYPE = "Basic"

async def verify_token_middleware(request: Request) -> TokenGeneratorTokenGenRequest | JSONResponse:
    mode = os.getenv("TEST_MODE")
    if mode is not None:
        return TokenGeneratorTokenGenRequest(id=1, role="admin")

    authorization = request.headers.get('Authorization')
    if authorization is None:
        return JSONResponse({"error": "unauthorized", "message": "cannot get token"},status_code=401)

    payload = authorization.split(" ")
    if len(payload) != 2:
        return JSONResponse({"error": "unauthorized", "message": "cannot get token"}, status_code=401)

    if payload[0] != JWT_TOKEN_TYPE:
        return JSONResponse({"error": "unauthorized", "message": "invalid token type"}, status_code=401)
    elif payload[0] != BASIC_TOKEN_TYPE:
        return JSONResponse({"error": "unauthorized", "message": "invalid token type"}, status_code=401)

    try:
        return await verify_token(payload[1])
    except ServiceUnavailableException as e:
        print("TokenGeneratorUnavailable, error: " + str(e))
        return JSONResponse({"error": "internal service error"}, status_code=500)

    except TokenVerifyException as e:
        return JSONResponse({"error": "unauthorized", "message": e.message}, status_code=401)

    except ValueError:
        print("VERIFY TOKEN ERROR: "+str(ValueError))
        return JSONResponse({"error": "internal service error"}, status_code=500)
    except Exception:
        print("UNEXPECTED ERROR: " + str(ValueError))
        return JSONResponse({"error": "internal service error"}, status_code=500)

async def only_internal_address_middleware(request: Request):
    header = request.headers.get('host')
    if header is None:
        return JSONResponse({"error": "unauthorized", "message": "cannot get token"}, status_code=401)

    if "products-service:8080" == header:
        return

    return JSONResponse(status_code=401, content={"error": "Access denied"})

