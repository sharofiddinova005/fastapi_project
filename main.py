from fastapi import FastAPI
from database import Base, engine

from auth.auth_router import auth_
from books.router import router as book_router
from comments.router import router as comment_router
from booking.router import router as booking_router

from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT
import logging

class Settings(BaseModel):
    authjwt_secret_key: str = "secret_kalit_soz_bu_yerda_123"


@AuthJWT.load_config
def get_config():
    return Settings()

logging.basicConfig(level=logging.INFO)

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "API ishlayapti"}

app.include_router(auth_, prefix="/auth")
app.include_router(book_router, prefix="/books")
app.include_router(comment_router, prefix="/comment")
app.include_router(booking_router, prefix="/booking")


