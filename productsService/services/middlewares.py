from fastapi import Request
from starlette.responses import JSONResponse

from productsService.clients.tokenGenerator import verify_token
from productsService.models.exception import ServiceUnavailableException, TokenVerifyException

JWT_TOKEN_TYPE = "Bearer"

async def verify_token_middleware(request: Request):
  authorization = request.headers.get('Authorization')
  if authorization is None:
      return JSONResponse({"error": "unauthorized", "message": "cannot get token"},status_code=401)

  payload = authorization.split(" ")
  if len(payload) != 2:
      return JSONResponse({"error": "unauthorized", "message": "cannot get token"}, status_code=401)

  if payload[0] != JWT_TOKEN_TYPE:
      return JSONResponse({"error": "unauthorized", "message": "invalid token type"}, status_code=401)

  try:
      await verify_token(payload[1])
  except ServiceUnavailableException as e:
      return JSONResponse({"error": "internal service error"}, status_code=500)

  except TokenVerifyException as e:
      return JSONResponse({"error": "unauthorized", "message": e.message}, status_code=401)

  except ValueError:
      print("VERIFY TOKEN ERROR: "+str(ValueError))
      return JSONResponse({"error": "internal service error"}, status_code=500)
  except Exception:
      return JSONResponse({"error": "internal service error"}, status_code=500)
  return


