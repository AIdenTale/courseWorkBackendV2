from starlette.responses import JSONResponse

from productsService.clients.kafka import send_new_product_to_kafka, send_new_card_to_kafka, send_deleted_card_to_kafka
from productsService.db.client import *
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

    card = ProductsCardModel(id=result[0], brand=card.brand, description=card.description, title=card.title)
    await send_new_card_to_kafka(card)

    return ProductsCardOutputModel(id=result[0])

async def edit_product_card(card: ProductsCardInputEditModel):
    try:
        edit_card(card)

        await send_new_card_to_kafka(card)

    except Exception as e:
        return JSONResponse(status_code=500, content={"internal server error": str(e)})

    return JSONResponse(status_code=200, content={"status": "ok"})

async def delete_product_card(card_id: int):
    try:
        delete_card(card_id)

        card = ProductsCardOutputModel(id=card_id)
        await send_deleted_card_to_kafka(card)

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

async def get_product_by_card_id_and_sku(card_id: int, sku: int):
    result = product_by_card_id_and_sku(card_id, sku)
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

    product = ProductModel(
        id=result[0],
        price=product.price,
        size=product.size,
        color=product.color,
        country=product.country,
        sku=product.sku,
    )
    await send_new_product_to_kafka(product)

    return ProductOutputModel(id=result[0])

async def edit_product_model(product: ProductsCardInputEditModel):
    try:
        edit_product(product)
        await send_new_product_to_kafka(product)

        return JSONResponse(status_code=200, content={"status": "ok"})
    except ForeignKeyViolation as e:
        return JSONResponse(status_code=400, content={"error": "Internal Server Error", "message": str(e)})
    except ZeroLinesUpdated as e:
        return JSONResponse(status_code=400, content={"error": "Validation Error", "message": str(e)})
    except ValueError as e:
        return JSONResponse(status_code=422, content={"error": "Невозможно изменить характеристики товара", "message": str(e)})

async def delete_product_model(product_id: int):
    try:
        delete_product(product_id)
    except ZeroLinesUpdated as e:
        return JSONResponse(status_code=400, content={"error": "Validation Error", "message": str(e)})
    except ValueError as e:
        return JSONResponse(status_code=422, content={"error": "Невозможно изменить характеристики товара", "message": str(e)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"internal server error": str(e)})

    return JSONResponse(status_code=200, content={"status": "ok"})

async def reserve_product_model(product_id: int):
    try:
        reserve_product(product_id)
    except Exception as e:
        return JSONResponse(status_code=500, content={"internal server error": str(e)})