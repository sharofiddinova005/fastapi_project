from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from comments.schemas import CommentCreate
from comments import crud

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/")
def create_comment(data: CommentCreate, db: Session = Depends(get_db)):
    return crud.create_comment(db, data)


@router.get("/book/{book_id}")
def get_book_comments(book_id: int, db: Session = Depends(get_db)):
    comments = crud.get_book_comments(db, book_id)

    if not comments:
        raise HTTPException(status_code=404, detail="Comment topilmadi")

    return comments
