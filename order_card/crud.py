from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from order_card.models import Cart, CartItem, Card
from order_card.schemas import CartItemCreate

from order_card.schema import CardCreate

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.post("/add")
def add_to_cart(user_id: int, data: CartItemCreate, db: Session = Depends(get_db)):

    cart = db.query(Cart).filter(Cart.user_id == user_id).first()

    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == data.product_id
    ).first()

    if item:
        item.quantity += data.quantity
    else:
        item = CartItem(
            cart_id=cart.id,
            product_id=data.product_id,
            quantity=data.quantity
        )
        db.add(item)

    db.commit()

    return {"message": "Mahsulot savatchaga qo'shildi"}


@router.delete("/remove")
def remove_from_cart(user_id: int, product_id: int, db: Session = Depends(get_db)):

    cart = db.query(Cart).filter(Cart.user_id == user_id).first()

    if not cart:
        raise HTTPException(404, "Savatcha topilmadi")

    item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == product_id
    ).first()

    if not item:
        raise HTTPException(404, "Mahsulot savatchada yo'q")

    db.delete(item)
    db.commit()

    return {"message": "Mahsulot savatchadan o'chirildi"}

@router.get("/")
def get_cart(user_id: int, db: Session = Depends(get_db)):

    cart = db.query(Cart).filter(Cart.user_id == user_id).first()

    if not cart:
        raise HTTPException(404, "Savatcha topilmadi")

    items = []

    for item in cart.items:
        items.append({
            "product_id": item.product_id,
            "quantity": item.quantity
        })

    return {
        "cart_id": cart.id,
        "items": items
    }

@router.post("/card/add")
def add_card(user_id: int, data: CardCreate, db: Session = Depends(get_db)):

    card = Card(
        user_id=user_id,
        card_number=data.card_number,
        card_holder=data.card_holder,
        expire_date=data.expire_date
    )

    db.add(card)
    db.commit()
    db.refresh(card)

    return {"message": "Karta qo'shildi"}