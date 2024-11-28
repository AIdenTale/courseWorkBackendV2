from fastapi import FastAPI
from ordersService.models import CreateOrder
from ordersService.services import OrderService

app = FastAPI()
service = OrderService()

@app.post("/orders")
def create_order(order: CreateOrder):
    order_id = service.create_order(order)
    return {"order_id": order_id}

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    order = service.get_order(order_id)
    if not order:
        return {"error": "Order not found"}
    return order
