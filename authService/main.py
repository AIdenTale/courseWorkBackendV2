from fastapi import FastAPI
from starlette.responses import JSONResponse

from authService.models.exceptions import EmailAlreadyRegistered
from authService.models.api import UserAuthReqModel, ErrorRespModel
from authService.services.services import AuthService

app = FastAPI()


@app.post("/register")
async def reqister(user: UserAuthReqModel):
    auth = AuthService()

    data = await auth.register_user(user)
    if isinstance(data, ErrorRespModel):
        return JSONResponse({"error": "internal error", "message": data.message}, status_code=500)
    elif isinstance(data, EmailAlreadyRegistered):
        return JSONResponse({"error": "ошибка пользователя", "message": str(EmailAlreadyRegistered)}, status_code=422)

    return data
