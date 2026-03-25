from pydantic import BaseModel


class CommentCreate(BaseModel):
    text: str
    book_id: int
    user_id: int


class CommentResponse(BaseModel):
    id: int
    text: str
    book_id: int
    user_id: int

    class Config:
        from_attributes = True