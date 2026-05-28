from typing import Optional
from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: Optional[str] = None
    mrp: Optional[str] = None
    image_url: Optional[str] = None
    benefits: Optional[str] = None
    ingredients: Optional[str] = None
    category_id: Optional[int] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    model_config = {'from_attributes': True}
