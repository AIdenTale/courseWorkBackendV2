from fastapi import FastAPI, Request

from productsService.services.middlewares import verify_token_middleware
from productsService.services.services import get_all_products

app = FastAPI()


@app.get("/products/all")
async def products_all(request: Request):
    result = await verify_token_middleware(request)
    if result is not None:
        return result

    return await get_all_products()
