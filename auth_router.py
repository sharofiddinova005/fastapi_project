from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import SignUpSchema, LoginSchema
from models import User
import auth
from fastapi_jwt_auth import AuthJWT
from fastapi import status
from werkzeug.security import check_password_hash

auth_ = APIRouter()


@auth_.post("/signup")
def sign_up(data: SignUpSchema, db: Session = Depends(get_db)):
    return auth.signup(db, data)


@auth_.post("/login")
def login(user: LoginSchema,
          Authorize: AuthJWT = Depends(),
          db: Session = Depends(get_db)):

    db_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if not db_user or not check_password_hash(db_user.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username yoki parol xato"
        )

    access_token = Authorize.create_access_token(subject=db_user.username)
    refresh_token = Authorize.create_refresh_token(subject=db_user.username)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


@auth_.get("/protected")
def protected(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()

    return {"user": current_user}