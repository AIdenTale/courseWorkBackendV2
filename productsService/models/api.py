from typing import List

from pydantic import BaseModel

class ProductModel(BaseModel):
    id: int
    brand: str
    price: float
    size: int
    color: str
    country: str

class ProductsCardModel(BaseModel):
    id: int
    title: str
    description: str
    count: int = None
    products: List[ProductModel] = None