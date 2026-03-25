from pydantic import BaseModel, Field
from typing import Optional


class ProductCreate(BaseModel):
    name: str = Field(min_length=3, max_length=20)
    description: Optional[str] = None
    price: int


class ProductResponse(ProductCreate):
    id: int

    class Config:
        from_attributes = True