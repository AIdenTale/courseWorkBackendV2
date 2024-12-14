from typing import Annotated

from pydantic import BaseModel, AfterValidator

from authService.utils.validators.str import required, email_required

class Error(BaseModel):
    message: str

class TokenGeneratorResponse(BaseModel):
    access_token: str

class TokenGeneratorTokenGenRequest(BaseModel):
    id: int
    role: str

class User(BaseModel):
    name: Annotated[str, AfterValidator(required)]
    surname: Annotated[str, AfterValidator(required)]
    email: Annotated[str, AfterValidator(required), AfterValidator(email_required)]
    role: str = None
    password: str = None

class LoginSuccessResponse(BaseModel):
    access_token: str

class UserLoginRequest(BaseModel):
    email: Annotated[str, AfterValidator(required), AfterValidator(email_required)]
    password: Annotated[str, AfterValidator(required)]

