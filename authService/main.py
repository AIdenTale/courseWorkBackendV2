from fastapi import FastAPI

from authService.models.api import UserAuthReqModel
from authService.services.services import AuthService

app = FastAPI()


@app.post("/register")
async def reqister(user: UserAuthReqModel):
    auth = AuthService()
    return await auth.register_user(user)
