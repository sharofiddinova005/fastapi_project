from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db, SessionLocal
from schemas import ProductCreate, ProductResponse
import crud

router = APIRouter()


@router.post("/")
def create(product:ProductCreate, db:Session = Depends(get_db)):
    return crud.create_product(db, product)

@router.get("/")
def get_all(db:Session = Depends(get_db)):
    return crud.get_all_products(db)

@router.get("/{product_id}")
def get_one(product_id: int, db: Session = Depends(get_db)):
    return crud.get_product(db, product_id)

@router.put("/{product_id}", response_model=ProductResponse)
def update(product_id: int, product:ProductCreate, db:Session = Depends(get_db)):
    updated = crud.update_product(db, product_id, product)
    # if not updated:
    #     raise HTTPException({'status_code':status, detail:"Product topilmadi"})
    # return updated

@router.delete("/{product_id}")
def delete(product_id: int, db:Session = Depends(get_db)):
    deleted = crud.delete_product(db, product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product topilmadi")
    return {"message": "Product o'chirildi"}




