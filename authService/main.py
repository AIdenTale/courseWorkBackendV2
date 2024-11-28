from fastapi import FastAPI

from models.api import UserAuthReqModel
from services.services import AuthService

app = FastAPI()


@app.post("/register")
async def reqister(user: UserAuthReqModel):
    auth = AuthService()
    return await auth.register_user(user)
