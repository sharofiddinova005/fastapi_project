from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from booking.schemas import BookingCreate
from booking import crud

router = APIRouter(prefix="/booking", tags=["Booking"])


@router.post("/")
def create_booking(data: BookingCreate, db: Session = Depends(get_db)):
    return crud.create_booking(db, data)


@router.get("/user/{user_id}")
def get_user_bookings(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user_bookings(db, user_id)