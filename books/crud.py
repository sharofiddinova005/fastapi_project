from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from books.models import Book, BookCategory
from auth.models import Genre
from books.schemas import ProductCreate


def create_product(db: Session, product: ProductCreate):
    new_product = Book(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product  # response_model ProductResponse uchun obyekt qaytariladi


def get_all_products(db: Session):
    return db.query(Book).all()  # list[Book], router response_model bilan mos


def get_product(db: Session, product_id: int):
    product = db.query(Book).filter(Book.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product topilmadi")
    return product


def update_product(db: Session, product_id: int, product: ProductCreate):
    db_product = db.query(Book).filter(Book.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product topilmadi")

    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price

    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int):
    db_product = db.query(Book).filter(Book.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product topilmadi")

    db.delete(db_product)
    db.commit()
    return db_product


def create_category(db: Session, name: str):
    category = BookCategory(name=name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def create_genre(db: Session, name: str):
    genre = Genre(name=name)
    db.add(genre)
    db.commit()
    db.refresh(genre)
    return genre