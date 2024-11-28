from typing import Annotated

from pydantic import BaseModel, AfterValidator

from tokenGeneratorService.utils.validators import required_str, required_int

class ErrorRespModel(BaseModel):
    message: str

class GenerateNewTokenReqModel(BaseModel):
    id: Annotated[int, AfterValidator(required_int)]
    role: Annotated[str, AfterValidator(required_str)]

class VerifyTokenReqModel(BaseModel):
    token: Annotated[str, AfterValidator(required_str)]

class VerifyTokenRespModel(BaseModel):
    id: int
    role: str

class UserAuthRespModel(BaseModel):
    access_token: str
