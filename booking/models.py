from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("book.id"))

    status = Column(String, default="bron qilingan")

    user = relationship("User")
    book = relationship("Book")