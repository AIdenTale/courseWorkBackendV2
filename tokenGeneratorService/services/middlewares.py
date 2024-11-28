from starlette.responses import JSONResponse
from fastapi import Request

from utils.exceptions import ValidationError
from utils.validators import validate_authorization_header


def authorization_middleware(request: Request):
    authorization = request.headers.get("Authorization")
    if authorization is None or len(authorization) == 0:
        return JSONResponse({"error": "invalid authorization"}, status_code=401)

    try:
        validate_authorization_header(authorization)
    except ValidationError as e:
        return JSONResponse({"error": "invalid authorization", "message": e.message}, status_code=401)
    except Exception as e:
        print(f"ERROR VALIDATING: {e}")
        return JSONResponse({"error": "internal error"}, status_code=500)

    return True