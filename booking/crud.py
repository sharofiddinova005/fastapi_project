from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from books import crud
from books.schemas import ProductCreate, ProductResponse
from database import get_db

router = APIRouter(prefix="/books", tags=["books"])

# --- Book CRUD ---
@router.post("/", response_model=ProductResponse)
def create_book(book: ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, book)

@router.get("/", response_model=list[ProductResponse])
def get_all_books(db: Session = Depends(get_db)):
    return crud.get_all_products(db)

@router.get("/{book_id}", response_model=ProductResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    return crud.get_product(db, book_id)

@router.put("/{book_id}", response_model=ProductResponse)
def update_book(book_id: int, book: ProductCreate, db: Session = Depends(get_db)):
    return crud.update_product(db, book_id, book)

@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    crud.delete_product(db, book_id)
    return {"message": "Kitob o'chirildi"}

# --- Category va Genre ---
@router.post("/category/")
def create_category(name: str, db: Session = Depends(get_db)):
    return crud.create_category(db, name)

@router.post("/genre/")
def create_genre(name: str, db: Session = Depends(get_db)):
    return crud.create_genre(db, name)