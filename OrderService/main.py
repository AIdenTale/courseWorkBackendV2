from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse
from ordersService.models import CreateOrder
from ordersService.services import OrderService

app = FastAPI()
service = OrderService()


@app.post("/create_order", status_code=201)
def create_order(order: CreateOrder):
    try:
        order_id = service.create_order(order)
        return JSONResponse(status_code=201)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Internal Server Error", "message": str(e)})


@app.get("/orders/{order_id}")
def get_order(order_id: int):
    order = service.get_order(order_id)
    if not order:
        return JSONResponse(status_code=204)  # Возвращаем 204 без текста
    return JSONResponse(status_code=200, content=order.dict())  # Преобразуем объект в словарь
