from pydantic import BaseModel


class BookingCreate(BaseModel):
    user_id: int
    book_id: int


class BookingResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    status: str

    class Config:
        from_attributes = True