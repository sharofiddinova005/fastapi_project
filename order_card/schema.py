from pydantic import BaseModel
from typing import List
from enum import Enum


class OrderStatus(str, Enum):
    new = "new"
    yetkazilyapti = "yetkazilyapti"
    done = "done"
    canceled = "canceled"

class CartaItem(BaseModel):
    product_id : int
    quantity : int = 1


class CartItemResponse(BaseModel):
    product_id: int
    quantity: int


class OrderCreate(BaseModel):
    pass

class CardCreate(BaseModel):
    card_number: str
    card_holder: str
    expire_date: str


class PaymentCreate(BaseModel):
    order_id: int
    card_id: int

# class OrderItemResponse(BaseModel):
#     product_id: int
#     quantity: int
#
#
# class OrderResponse(BaseModel):
#     id: int
#     status: OrderStatus
#     items: List[OrderItemResponse]

