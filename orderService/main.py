from fastapi import FastAPI, Request

app = FastAPI()


@app.post("/create_order")
async def create_order(verifyModel: VerifyTokenReqModel):
    data = await verify_token(verifyModel.token)
    if isinstance(data, ErrorRespModel):
        return JSONResponse({"error": "validation error", "message": data.message}, status_code=400)

    return data