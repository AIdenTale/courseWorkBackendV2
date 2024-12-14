from pydantic import BaseModel

class ProductModel(BaseModel):
    id: int
    price: float
    size: int
    color: str
    country: str
    sku: int