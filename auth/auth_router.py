from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth.schemas import SignUpSchema, LoginSchema, ProfileUpdateSchema
from database import get_db
from . import auth as auth_service
from fastapi_jwt_auth import AuthJWT

auth_ = APIRouter()


@auth_.post("/signup")
def signup(user: SignUpSchema, db: Session = Depends(get_db)):
    return auth_service.signup(db, user)


@auth_.post("/login")
async def login(data: LoginSchema, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    return auth_service.login_user(db, data, Authorize)


@auth_.get("/refresh")
def refresh_token(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    return auth_service.refresh_access_token(db, Authorize)


@auth_.get("/profile")
def profile(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    return auth_service.profile(db, Authorize)


@auth_.put("/profile")
def update_profile(update_data: ProfileUpdateSchema, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    return auth_service.update_profile(db, update_data, Authorize)

