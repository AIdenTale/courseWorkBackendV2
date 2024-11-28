from typing import Annotated

from pydantic import BaseModel, AfterValidator

from authService.utils.validators.str import required, email_required

class ErrorRespModel(BaseModel):
    message: str

class TokenGeneratorServiceRespModel(BaseModel):
    access_token: str

class UserAuthReqModel(BaseModel):
    name: Annotated[str, AfterValidator(required)]
    surname: Annotated[str, AfterValidator(required)]
    email: Annotated[str, AfterValidator(required), AfterValidator(email_required)]
    password: Annotated[str, AfterValidator(required)]

class UserAuthRespModel(BaseModel):
    access_token: str