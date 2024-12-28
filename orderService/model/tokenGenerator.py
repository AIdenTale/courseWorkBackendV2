from pydantic import BaseModel


class TokenGeneratorTokenGenRequest(BaseModel):
    id: int
    role: str

class ServiceUnavailableException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class TokenVerifyException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message