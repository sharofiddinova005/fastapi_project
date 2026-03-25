from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class BookCategory(Base):
    __tablename__ = "book_category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    books = relationship("Book", back_populates="category")


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("book_category.id", ondelete="RESTRICT"), nullable=False)
    genre_id = Column(Integer, ForeignKey("genres.id"))
    name = Column(String(100), nullable=False)
    description = Column(String, nullable=True)
    price = Column(Integer, nullable=False)

    owner = relationship("User", back_populates="books")
    category = relationship("BookCategory", back_populates="books")
    genre = relationship("Genre", back_populates="books")