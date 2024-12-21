from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from authService.models.api import User, Error, UserLoginRequest
from authService.models.exceptions import EmailAlreadyRegistered
from authService.services.middlewares import verify_token_middleware
from authService.services.services import register_user, auth_user, get_user_profile

app = FastAPI()
@app.post("/register")
async def reqister(user: User):
    data = await register_user(user)
    if isinstance(data, Error):
        return JSONResponse({"error": "internal error", "message": data.message}, status_code=500)
    elif isinstance(data, EmailAlreadyRegistered):
        return JSONResponse({"error": "ошибка пользователя", "message": str(EmailAlreadyRegistered)}, status_code=422)

    return data

@app.post("/auth")
async def auth(user: UserLoginRequest):
    data = await auth_user(user)
    if isinstance(data, Error):
        return JSONResponse({"error": "internal error", "message": data.message}, status_code=500)
    elif isinstance(data, EmailAlreadyRegistered):
        return JSONResponse({"error": "ошибка пользователя", "message": str(EmailAlreadyRegistered)}, status_code=422)

    return data
@app.get("/profile")
async def profile(request: Request):
    result = await verify_token_middleware(request)
    if isinstance(result, JSONResponse):
        return result
    data = await get_user_profile(result)
    if isinstance(data, Error):
        return JSONResponse({"error": "internal error", "message": data.message}, status_code=500)

    return data
