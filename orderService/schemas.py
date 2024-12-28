from pydantic import BaseModel
from typing import List, Optional

# Товар в заказе
class OrderProductSchema(BaseModel):
    price: float
    size: Optional[str]
    color: Optional[str]
    country: Optional[str]
    sku: int
    card_id: Optional[int]

# Создание заказа
class OrderCreateSchema(BaseModel):
    user_id: int
    total_amount: float
    products: List[OrderProductSchema]

# Ответ по заказу
class OrderResponseSchema(BaseModel):
    id: int
    user_id: int
    order_date: str
    status: str
    total_amount: float
    products: List[OrderProductSchema]

    class Config:
        orm_mode = True
