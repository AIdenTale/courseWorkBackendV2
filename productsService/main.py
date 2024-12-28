from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from productsService.models.api import *
from productsService.services.middlewares import *
from productsService.services.services import *

app = FastAPI()


@app.get("/cards/all")
async def cards_all(request: Request):
    result = await verify_token_middleware(request)
    if isinstance(result, JSONResponse):
        return result

    return await get_all_products_cards()

@app.get("/cards/by_id")
async def cards_by_id(request: Request, card_id: int):
    result = await verify_token_middleware(request)
    if isinstance(result, JSONResponse):
        return result

    return await get_products_card_by_id(card_id)

@app.post("/cards/new")
async def cards_new(request: Request, card: ProductsCardInputModel):
    result = await verify_token_middleware(request)
    if isinstance(result, JSONResponse):
        return result
    elif isinstance(result, TokenGeneratorTokenGenRequest):
        if result.role != "admin":
            return JSONResponse(status_code=401, content={"error": "Access denied"})

    return await add_product_card(card)

@app.post("/cards/update")
async def cards_update(request: Request, card: ProductsCardInputEditModel):
    result = await verify_token_middleware(request)
    if isinstance(result, JSONResponse):
        return result
    elif isinstance(result, TokenGeneratorTokenGenRequest):
        if result.role != "admin":
            return JSONResponse(status_code=401, content={"error": "Access denied"})

    if card.title is None and card.description is None and card.brand is None:
        return JSONResponse(status_code=400, content={"error": "Missing required fields"})

    return await edit_product_card(card)
@app.get("/cards/delete")
async def cards_update(request: Request, card_id: int):
    result = await verify_token_middleware(request)
    if isinstance(result, JSONResponse):
        return result
    elif isinstance(result, TokenGeneratorTokenGenRequest):
        if result.role != "admin":
            return JSONResponse(status_code=401, content={"error": "Access denied"})

    return await delete_product_card(card_id)

@app.get("/products/all")
async def products_all(request: Request):
    result = await verify_token_middleware(request)
    if isinstance(result, JSONResponse):
        return result

    return await get_all_products()

@app.get("/products/by_id")
async def products_by_id(request: Request, product_id: int):
    result = await verify_token_middleware(request)
    if isinstance(result, JSONResponse):
        return result

    return get_products_by_id(product_id)

@app.get("/products/by_card_id_and_sku")
async def products_by_card_and_and_sku(request: Request, card_id: int, sku: int):
    result = await verify_token_middleware(request)
    if isinstance(result, JSONResponse):
        return result

    return await get_product_by_card_id_and_sku(card_id, sku)

@app.post("/products/new")
async def products_new(request: Request, product: ProductInputModel):
    result = await verify_token_middleware(request)
    if isinstance(result, JSONResponse):
        return result
    elif isinstance(result, TokenGeneratorTokenGenRequest):
        if result.role != "admin":
            return JSONResponse(status_code=401, content={"error": "Access denied"})

    return await add_product(product)

@app.post("/products/edit")
async def products_edit(request: Request, product: ProductInputEditModel):
    result = await verify_token_middleware(request)
    if isinstance(result, JSONResponse):
        return result
    elif isinstance(result, TokenGeneratorTokenGenRequest):
        if result.role != "admin":
            return JSONResponse(status_code=401, content={"error": "Access denied"})

    if product.color is None and \
    product.country is None and \
    product.price is None and \
    product.sku is None and \
    product.size is None and \
    product.card_id is None:
        return JSONResponse(status_code=400, content={"error": "Missing required fields"})

    return await edit_product_model(product)

@app.get("/products/delete")
async def products_delete(request: Request, product_id: int):
    result = await verify_token_middleware(request)
    if isinstance(result, JSONResponse):
        return result
    elif isinstance(result, TokenGeneratorTokenGenRequest):
        if result.role != "admin":
            return JSONResponse(status_code=401, content={"error": "Access denied"})

    return await delete_product_model(product_id)

@app.get("/cards/reserve")
async def reserve_cards(product_id: int):
    return await reserve_product_model(product_id)

