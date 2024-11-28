from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from tokenGeneratorService.models.api import GenerateNewTokenReqModel, VerifyTokenReqModel, ErrorRespModel
from tokenGeneratorService.services.middlewares import authorization_middleware
from tokenGeneratorService.services.services import generate_new_token, verify_token

app = FastAPI()

@app.post("/jwt/generate_new")
async def generate_new_token_handler(request: Request, genModel: GenerateNewTokenReqModel):
    process_data = authorization_middleware(request)
    if isinstance(process_data, JSONResponse):
        return process_data

    data = await generate_new_token(genModel.id, genModel.role)
    if isinstance(data, ErrorRespModel):
        return JSONResponse({"error": "internal error"}, status_code=500)

    return data

@app.post("/jwt/verify")
async def verify_token_handler(verifyModel: VerifyTokenReqModel):
    data = await verify_token(verifyModel.token)
    if isinstance(data, ErrorRespModel):
        return JSONResponse({"error": "validation error", "message": data.message}, status_code=400)

    return data