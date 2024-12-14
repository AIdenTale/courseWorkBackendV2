from pydantic import BaseModel

class ProductModel(BaseModel):
    id: int
    title: str
    brand: str
    price: float
    size: int
    color: str
    country: str


