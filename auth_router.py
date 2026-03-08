from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import SignUpSchema, LoginSchema, ProfileUpdateSchema
import auth
from fastapi_jwt_auth import AuthJWT

auth_ = APIRouter()


@auth_.post("/signup")
def signup(user: SignUpSchema, db: Session = Depends(get_db)):
    return auth.signup(db, user)


@auth_.post("/login")
def login(user: LoginSchema, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    return auth.login_user(db, user, Authorize)


@auth_.get("/refresh")
def refresh_token(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    return auth.refresh_access_token(db, Authorize)


@auth_.get("/profile")
def profile(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    return auth.profile(db, Authorize)


@auth_.put("/profile")
def update_profile(update_data: ProfileUpdateSchema, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    return auth.update_profile(db, update_data, Authorize)