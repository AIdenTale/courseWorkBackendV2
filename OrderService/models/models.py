from pydantic import BaseModel
from typing import List

class OrderItem(BaseModel):
    product_id: int
    quantity: int

class CreateOrder(BaseModel):
    user_id: int
    items: List[OrderItem]

class OrderResponse(BaseModel):
    order_id: int
    user_id: int
    status: str
    created_at: str
    items: List[OrderItem]
