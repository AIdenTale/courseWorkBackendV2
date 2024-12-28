from typing import Annotated, Optional

from pydantic import BaseModel, AfterValidator

from orderService.model.validators.validators import required_int, required_list

INT_LIMIT = 2147483647

class ProductInfoInputModel(BaseModel):
    card_id: Annotated[int, AfterValidator(required_int)]
    sku: Annotated[int, AfterValidator(lambda v: v if INT_LIMIT > v > 0 else None), AfterValidator(required_int)]

class CreateOrderInputModel(BaseModel):
    products: Annotated[list[ProductInfoInputModel], AfterValidator(required_list)]


class ProductInfoInOrder(BaseModel):
    id: int
    price: Optional[float | None] = None
    size: Optional[int | None] = None
    color: Optional[str | None] = None
    country: Optional[str | None] = None
    sku: Optional[int | None] = None

class ProductInfo(BaseModel):
    id: int
    price: float
    size: int
    color: str
    country: str
    sku: int

class OrderInfo(BaseModel):
    order_id: int
    user_id: int
    order_date: str
    status: str
    total_amount: int
    products: list[ProductInfo]


class OrderInfoToProducts(BaseModel):
    order_id: int
    user_id: int
    order_date: str
    status: str
    total_amount: int
    products: list[ProductInfoInOrder]