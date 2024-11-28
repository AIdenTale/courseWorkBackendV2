from pydantic import BaseModel

class ProductModel(BaseModel):
    id: int
    brand: str
    price: float
    size: int
    color: str
    country: str