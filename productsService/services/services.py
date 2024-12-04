from starlette.responses import JSONResponse

from productsService.db.client import create_new_card, all_products_cards, product_card_by_id, edit_card, delete_card, \
    create_new_product, all_products, product_by_id, edit_product, delete_product
from productsService.models.api import ProductsCardInputModel, ProductsCardOutputModel, ProductsCardInputEditModel, \
    ProductInputModel, ProductOutputModel
from productsService.models.exception import ForeignKeyViolation, ZeroLinesUpdated


async def get_all_products_cards():
    return all_products_cards()

async def get_products_card_by_id(id: int):
    result = product_card_by_id(id)
    if result is None:
        return JSONResponse(status_code=204, content=None)

    return result

async def add_product_card(card: ProductsCardInputModel):
    result = create_new_card(card)
    return ProductsCardOutputModel(id=result[0])

async def edit_product_card(card: ProductsCardInputEditModel):
    try:
        edit_card(card)
    except Exception as e:
        return JSONResponse(status_code=500, content={"internal server error": str(e)})

    return JSONResponse(status_code=200, content={"status": "ok"})

async def delete_product_card(card_id: int):
    try:
        delete_card(card_id)
    except ZeroLinesUpdated as e:
        return JSONResponse(status_code=400, content={"error": "Validation Error", "message": str(e)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"internal server error": str(e)})

    return JSONResponse(status_code=200, content={"status": "ok"})




async def get_all_products():
    return all_products()

async def get_products_by_id(id: int):
    result = product_by_id(id)
    if result is None:
        return JSONResponse(status_code=204, content=None)

    return result

async def add_product(product: ProductInputModel):
    try:
        result = create_new_product(product)
    except ForeignKeyViolation as e:
        return JSONResponse(status_code=400, content={"error": "Internal Server Error", "message": str(e)})
    except Exception as e:
        print(f"DataBase error: {e}")
        return JSONResponse(status_code=500, content={"error": "Internal Server Error"})
    return ProductOutputModel(id=result[0])

async def edit_product_model(card: ProductsCardInputEditModel):
    try:
        edit_product(card)
        return JSONResponse(status_code=200, content={"status": "ok"})
    except ForeignKeyViolation as e:
        return JSONResponse(status_code=400, content={"error": "Internal Server Error", "message": str(e)})
    except ZeroLinesUpdated as e:
        return JSONResponse(status_code=400, content={"error": "Validation Error", "message": str(e)})

async def delete_product_model(product_id: int):
    try:
        delete_product(product_id)
    except ZeroLinesUpdated as e:
        return JSONResponse(status_code=400, content={"error": "Validation Error", "message": str(e)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"internal server error": str(e)})

    return JSONResponse(status_code=200, content={"status": "ok"})
