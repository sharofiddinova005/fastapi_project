from pydantic import BaseModel, Field
from typing import Optional


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

class ProfileUpdateSchema(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[str] = None