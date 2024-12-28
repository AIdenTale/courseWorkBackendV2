import datetime

from pydantic import BaseModel
from typing import List, Optional

# Товар в заказе
class OrderProductSchema(BaseModel):
    product_id: int
    card_id: int

# Создание заказа
class OrderCreateSchema(BaseModel):
    user_id: int
    products: List[OrderProductSchema]

# Ответ по заказу
class OrderResponseSchema(BaseModel):
    id: int
    user_id: int
    order_date: datetime.datetime
    status: str
    total_amount: float
    products: List[OrderProductSchema]

    class Config:
        orm_mode = True


class OrderProductSchemaDetailed(BaseModel):
    product_id: int
    card_id: int
    sku: int
    price: float
    country: str
    size: int

class OrderResponseSchemaDetailed(BaseModel):
    id: int
    user_id: int
    order_date: datetime.datetime
    status: str
    total_amount: float
    products: List[OrderProductSchemaDetailed]

    class Config:
        orm_mode = True