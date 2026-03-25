from sqlalchemy.orm import Session
from comments.models import Comment


def create_comment(db: Session, data):
    comment = Comment(**data.dict())
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def get_book_comments(db: Session, book_id: int):
    return db.query(Comment).filter(Comment.book_id == book_id).all()

