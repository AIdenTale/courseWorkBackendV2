from typing import List, Annotated

from pydantic import BaseModel, AfterValidator

from productsService.utils.validators.str import required
from productsService.utils.validators.float import required_float
from productsService.utils.validators.int import required_int


class ProductModel(BaseModel):
    id: int = None
    brand: str
    price: float
    size: str
    color: str
    country: str

class ProductInputModel(BaseModel):
    brand: Annotated[str, AfterValidator(lambda v: v if 500 >= len(v) > 1 else None), AfterValidator(required)]
    price: Annotated[float,  AfterValidator(lambda v: v if 100 <= v <= 100000 else None), AfterValidator(required_float)]
    size: Annotated[int, AfterValidator(lambda v: v if 10 <= v <= 70 else None), AfterValidator(required_int)]
    color: Annotated[str, AfterValidator(lambda v: v if 50 >= len(v) > 0 else None), AfterValidator(required)]
    country: Annotated[str, AfterValidator(lambda v: v if len(v) == 2 else None), AfterValidator(required)]
    card_id: Annotated[int, AfterValidator(required_int)]

class ProductInputEditModel(BaseModel):
    id: Annotated[int, AfterValidator(required_int)]
    brand: Annotated[str | None, AfterValidator(lambda v: v if 500 >= len(v) > 1 else None)] = None
    price: Annotated[float | None,  AfterValidator(lambda v: v if 100 <= v <= 100000 else None)] = None
    size: Annotated[int | None, AfterValidator(lambda v: v if 10 <= v <= 70 else None)] = None
    color: Annotated[str | None, AfterValidator(lambda v: v if 50 >= len(v) > 0 else None)] = None
    country: Annotated[str | None, AfterValidator(lambda v: v if len(v) == 2 else None)] = None
    card_id: Annotated[int | None, AfterValidator(lambda v: v if v > 0 else None)] = None

class ProductOutputModel(BaseModel):
    id: int

class ProductsCardInputModel(BaseModel):
    title: Annotated[str, AfterValidator(lambda v: v if 2 < len(v) <= 500 else None), AfterValidator(required)]
    description: Annotated[str, AfterValidator(lambda v: v if 2 < len(v) <= 500 else None), AfterValidator(required)]

class ProductsCardInputEditModel(BaseModel):
    id: Annotated[int, AfterValidator(required_int)]
    title: Annotated[str | None, AfterValidator(lambda v: v if 2 < len(v) <= 500 else None)] = None
    description: Annotated[str | None, AfterValidator(lambda v: v if 2 < len(v) <= 500 else None)] = None

class ProductsCardOutputModel(BaseModel):
    id: int

class ProductsCardModel(BaseModel):
    id: int
    title: str
    description: str
    count: int = None
    products: List[ProductModel] = None