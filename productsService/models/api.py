from typing import List, Annotated

from pydantic import BaseModel, AfterValidator

from productsService.utils.validators.str import required
from productsService.utils.validators.float import required_float
from productsService.utils.validators.int import required_int

INT_LIMIT = 2147483647

class TokenGeneratorTokenGenRequest(BaseModel):
    id: int
    role: str

class ProductModel(BaseModel):
    id: int = None
    price: float
    size: str
    color: str
    country: str
    sku: int
    is_reserved: bool = None

class ProductInputModel(BaseModel):
    price: Annotated[float,  AfterValidator(lambda v: v if 100 <= v <= 100000 else None), AfterValidator(required_float)]
    size: Annotated[int, AfterValidator(lambda v: v if 10 <= v <= 70 else None), AfterValidator(required_int)]
    color: Annotated[str, AfterValidator(lambda v: v if 50 >= len(v) > 0 else None), AfterValidator(required)]
    country: Annotated[str, AfterValidator(lambda v: v if len(v) == 2 else None), AfterValidator(required)]
    card_id: Annotated[int, AfterValidator(required_int)]
    sku: Annotated[int, AfterValidator(lambda v: v if INT_LIMIT > v > 0 else None), AfterValidator(required_int)]

class ProductInputEditModel(BaseModel):
    id: Annotated[int, AfterValidator(required_int)]
    price: Annotated[float,  AfterValidator(lambda v: v if 100 <= v <= 100000 else None)] = None
    size: Annotated[int, AfterValidator(lambda v: v if 10 <= v <= 70 else None)] = None
    color: Annotated[str, AfterValidator(lambda v: v if 50 >= len(v) > 0 else None)] = None
    country: Annotated[str, AfterValidator(lambda v: v if len(v) == 2 else None)] = None
    card_id: Annotated[int, AfterValidator(lambda v: v if INT_LIMIT > v > 0 else None)] = None
    sku: Annotated[int, AfterValidator(lambda v: v if INT_LIMIT > v > 0 else None)] = None

class ProductOutputModel(BaseModel):
    id: int

class ProductsCardInputModel(BaseModel):
    title: Annotated[str, AfterValidator(lambda v: v if 2 < len(v) <= 500 else None), AfterValidator(required)]
    description: Annotated[str, AfterValidator(lambda v: v if 2 < len(v) <= 500 else None), AfterValidator(required)]
    brand: Annotated[str, AfterValidator(lambda v: v if 500 >= len(v) > 1 else None), AfterValidator(required)]

class ProductsCardInputEditModel(BaseModel):
    id: Annotated[int, AfterValidator(required_int)]
    title: Annotated[str, AfterValidator(lambda v: v if 2 < len(v) <= 500 else None)] = None
    description: Annotated[str, AfterValidator(lambda v: v if 2 < len(v) <= 500 else None)] = None
    brand: Annotated[str, AfterValidator(lambda v: v if 500 >= len(v) > 1 else None)] = None

class ProductsCardOutputModel(BaseModel):
    id: int

class ProductsCardModel(BaseModel):
    id: int
    title: str
    description: str
    brand: str
    count: int = None
    products: List[ProductModel] = None