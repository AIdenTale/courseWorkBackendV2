import datetime

import sqlalchemy
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import JSONResponse

from orderService.clients.productsService import get_products_byid, reverve_products
from orderService.database import SessionLocal
from orderService.kafka_producer import send_kafka_event
from orderService.middlewares import verify_token_middleware
from orderService.model.models import OrderInfo, ProductInfo, ProductInfoInOrder, OrderInfoToProducts
from orderService.model.tokenGenerator import TokenGeneratorTokenGenRequest
from orderService.models import Order, OrderProduct
from orderService.schemas import OrderResponseSchema, OrderCreateSchema, OrderResponseSchemaDetailed

app = FastAPI(title="Order Service")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/", response_model=OrderResponseSchema)
async def create_order(request: Request, order: OrderCreateSchema, db: Session = Depends(get_db)):
    result = await verify_token_middleware(request)
    if isinstance(result, JSONResponse):
        return result

    new_order = Order(
        user_id=order.user_id,
        order_date=datetime.datetime.now(),
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for product in order.products:
        new_product = OrderProduct(
            order_id=new_order.id,
            product_id=product.product_id,
            card_id=product.card_id
        )
        db.add(new_product)
    try:
        db.commit()
    except sqlalchemy.exc.ProgrammingError:
        return JSONResponse(status_code=401, content={"error": "Access denied"})

    ids = []
    for product in order.products:
        ids.append(product.product_id)

    await reverve_products(ids)

    # send_kafka_event('orders-created', {'order_id': new_order.id})


    return new_order


# 📌 2. Удаление заказа
@app.delete("/{order_id}")
async def delete_order(request: Request, order_id: int, db: Session = Depends(get_db)):
    result = await verify_token_middleware(request)
    if isinstance(result, JSONResponse):
        return result
    elif isinstance(result, TokenGeneratorTokenGenRequest):
        if result.role != "admin":
            return JSONResponse(status_code=401, content={"error": "Access denied"})

    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
    # send_kafka_event('orders-deleted', {'order_id': order_id})
    return {"message": f"Order {order_id} deleted"}


@app.get("/orders", response_model=list[OrderResponseSchema] | OrderResponseSchema)
async def get_order(request: Request, db: Session = Depends(get_db)):
    result = await verify_token_middleware(request)
    if isinstance(result, JSONResponse):
        return result

    order = db.query(Order).filter(Order.user_id == result.id).all()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.get("/orders/detailed")
async def get_order(request: Request, db: Session = Depends(get_db)):
    result = await verify_token_middleware(request)
    if isinstance(result, JSONResponse):
        return result

    orders = db.query(Order).filter(Order.user_id == result.id).all()
    if not orders:
        raise HTTPException(status_code=204, detail="Order not found")

    formatted_orders = orders[:]
    orders = []
    for order in formatted_orders:
        products = []
        for product in order.products:
            products.append(ProductInfoInOrder(
                id=product.product_id,
            ))

        orders.append(OrderInfoToProducts(
          order_id=order.id,
            user_id=order.user_id,
            order_date=order.order_date.strftime("%Y-%m-%d"),
            status=order.status,
            total_amount=order.total_amount,
            products=products,
        ))

    for order in orders:
        products_ids = []
        for product in order.products:
            products_ids.append(product.id)

        data = await get_products_byid(products_ids)
        if not data:
            raise HTTPException(status_code=204, detail="Product not found")

        order.products = data

    return orders
