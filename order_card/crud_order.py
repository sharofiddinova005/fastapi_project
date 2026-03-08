from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from order_card.models import Cart, CartItem, Order, OrderItem

router = APIRouter(prefix="/order", tags=["Order"])


@router.post("/create")
def create_order(user_id: int, db: Session = Depends(get_db)):

    cart = db.query(Cart).filter(Cart.user_id == user_id).first()

    if not cart or not cart.items:
        raise HTTPException(400, "Savatcha bo'sh")

    order = Order(user_id=user_id)

    db.add(order)
    db.commit()
    db.refresh(order)

    for item in cart.items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(order_item)

    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()

    db.commit()

    return {"message": "Buyurtma yaratildi", "order_id": order.id}

@router.get("/")
def get_orders(user_id: int, db: Session = Depends(get_db)):

    orders = db.query(Order).filter(Order.user_id == user_id).all()

    result = []

    for order in orders:

        items = []

        for item in order.items:
            items.append({
                "product_id": item.product_id,
                "quantity": item.quantity
            })

        result.append({
            "order_id": order.id,
            "status": order.status,
            "items": items
        })

    return result


@router.patch("/status")
def update_order_status(order_id: int, status: str, db: Session = Depends(get_db)):

    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(404, "Order topilmadi")

    order.status = status

    db.commit()

    return {"message": "Order status yangilandi"}


@router.post("/pay")
def pay_order(data: PaymentCreate, db: Session = Depends(get_db)):

    order = db.query(Order).filter(Order.id == data.order_id).first()

    if not order:
        raise HTTPException(404, "Order topilmadi")

    payment = Payment(
        order_id=data.order_id,
        card_id=data.card_id
    )

    order.status = "done"

    db.add(payment)
    db.commit()

    return {"message": "To'lov muvaffaqiyatli bajarildi"}