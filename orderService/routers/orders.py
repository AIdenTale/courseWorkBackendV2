from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from orderService.database import SessionLocal
from orderService.models import Order, OrderProduct
from orderService.schemas import OrderCreateSchema, OrderResponseSchema
from orderService.kafka_producer import send_kafka_event

router = APIRouter(prefix="/orders", tags=["Orders"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 📌 1. Создание заказа
@router.post("/", response_model=OrderResponseSchema)
def create_order(order: OrderCreateSchema, db: Session = Depends(get_db)):
    new_order = Order(user_id=order.user_id, total_amount=order.total_amount)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for product in order.products:
        new_product = OrderProduct(
            order_id=new_order.id,
            price=product.price,
            size=product.size,
            color=product.color,
            country=product.country,
            sku=product.sku,
            card_id=product.card_id
        )
        db.add(new_product)
    db.commit()

    send_kafka_event('orders-created', {'order_id': new_order.id})
    return new_order


# 📌 2. Удаление заказа
@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
    send_kafka_event('orders-deleted', {'order_id': order_id})
    return {"message": f"Order {order_id} deleted"}


# 📌 3. Получение заказа по ID
@router.get("/{order_id}", response_model=OrderResponseSchema)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


# 📌 4. Получение всех заказов
@router.get("/", response_model=List[OrderResponseSchema])
def get_all_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    return orders
