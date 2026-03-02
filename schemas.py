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


# -------- USER --------

class SignUpSchema(BaseModel):
    name: str
    age: int
    username: str = Field(min_length=5, max_length=20)
    password: str = Field(min_length=5, max_length=20)
    email: str

class LoginSchema(BaseModel):
    username: str
    password: str


class Settings(BaseModel):
    authjwt_secret_key: str = "b741ce2262b74eef54c095aa541ed97d67c636b83e8c2ebad36feccf56643bef"




