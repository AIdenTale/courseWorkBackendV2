from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from productsService.models.api import ProductInputModel, ProductsCardInputEditModel, ProductsCardInputModel, \
    ProductInputEditModel
from productsService.services.middlewares import verify_token_middleware
from productsService.services.services import get_all_products_cards, get_products_card_by_id, add_product_card, \
    edit_product_card, \
    delete_product_card, add_product, get_all_products, get_products_by_id, edit_product_model, delete_product_model

app = FastAPI()


@app.get("/cards/all")
async def cards_all(request: Request):
    result = await verify_token_middleware(request)
    if result is not None:
        return result

    return await get_all_products_cards()

@app.get("/cards/by_id")
async def products_by_id(request: Request, card_id: int):
    result = await verify_token_middleware(request)
    if result is not None:
        return result

    return await get_products_card_by_id(card_id)

@app.post("/cards/new")
async def cards_new(request: Request, card: ProductsCardInputModel):
    result = await verify_token_middleware(request)
    if result is not None:
        return result

    return await add_product_card(card)

@app.post("/cards/update")
async def cards_update(request: Request, card: ProductsCardInputEditModel):
    result = await verify_token_middleware(request)
    if result is not None:
        return result

    if card.title is None and card.description is None:
        return JSONResponse(status_code=400, content={"error": "Missing required fields"})

    return await edit_product_card(card)

@app.get("/cards/delete")
async def cards_update(request: Request, card_id: int):
    result = await verify_token_middleware(request)
    if result is not None:
        return result

    return await delete_product_card(card_id)


@app.get("/products/all")
async def products_all(request: Request):
    result = await verify_token_middleware(request)
    if result is not None:
        return result

    return await get_all_products()

@app.get("/products/by_id")
async def products_by_id(request: Request, product_id: int):
    result = await verify_token_middleware(request)
    if result is not None:
        return result

    return await get_products_by_id(product_id)

@app.post("/products/new")
async def products_new(request: Request, product: ProductInputModel):
    result = await verify_token_middleware(request)
    if result is not None:
        return result

    return await add_product(product)

@app.post("/products/edit")
async def products_new(request: Request, product: ProductInputEditModel):
    result = await verify_token_middleware(request)
    if result is not None:
        return result

    if product.color is None and \
    product.country is None and \
    product.price is None and \
    product.brand is None and \
    product.size is None and \
    product.card_id is None:
        return JSONResponse(status_code=400, content={"error": "Missing required fields"})

    return await edit_product_model(product)

@app.get("/products/delete")
async def products_update(request: Request, product_id: int):
    result = await verify_token_middleware(request)
    if result is not None:
        return result

    return await delete_product_model(product_id)

@app.get("/test")
async def test(request: Request):
    return request.headers