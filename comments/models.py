from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


from database import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    text = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("book.id"))

    user = relationship("User")
    book = relationship("Book")