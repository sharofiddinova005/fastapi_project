from sqlalchemy.orm import Session
from .models import User
from .schemas import SignUpSchema, LoginSchema, ProfileUpdateSchema
from fastapi import HTTPException, status, Depends
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

# ---------------- SIGNUP ----------------
def signup(db: Session, data: SignUpSchema):
    db_user = db.query(User).filter(
        (User.username == data.username) | (User.email == data.email)
    ).first()

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username yoki email mavjud"
        )

    new_user = User(
        name=data.name,
        age=data.age,
        username=data.username,
        email=data.email,
        password=generate_password_hash(data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return jsonable_encoder({
        "status": 201,
        "message": "User yaratildi",
        "username": new_user.username
    })


# ---------------- LOGIN ----------------
def login_user(db: Session, data: LoginSchema, Authorize: AuthJWT):
    user = db.query(User).filter(
        (User.username == data.username) | (User.email == data.username)
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="Foydalanuvchi topilmadi")

    if not check_password_hash(user.password, data.password):
        raise HTTPException(status_code=401, detail="Parol noto'g'ri")

    access_token = Authorize.create_access_token(subject=str(user.username))
    refresh_token = Authorize.create_refresh_token(subject=str(user.username))

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "username": user.username
    }


# ---------------- REFRESH TOKEN ----------------
def refresh_access_token(db: Session, Authorize: AuthJWT):
    try:
        Authorize.jwt_refresh_token_required()
        current_user = Authorize.get_jwt_subject()
        new_access_token = Authorize.create_access_token(subject=current_user)
        return jsonable_encoder({"access_token": new_access_token})
    except AuthJWTException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


# ---------------- GET PROFILE ----------------
def profile(db: Session, Authorize: AuthJWT):
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()
        user = db.query(User).filter(User.username == current_user).first()
        if not user:
            raise HTTPException(status_code=404, detail="User topilmadi")
        return jsonable_encoder({
            "username": user.username,
            "email": user.email,
            "name": user.name,
            "age": user.age
        })
    except AuthJWTException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


# ---------------- UPDATE PROFILE ----------------
def update_profile(db: Session, data: ProfileUpdateSchema, Authorize: AuthJWT):
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()
        user = db.query(User).filter(User.username == current_user).first()
        if not user:
            raise HTTPException(status_code=404, detail="User topilmadi")

        # Update fields if provided
        if data.name:
            user.name = data.name
        if data.age:
            user.age = data.age
        if data.email:
            # Email uniqueness check
            if db.query(User).filter(User.email == data.email, User.id != user.id).first():
                raise HTTPException(status_code=400, detail="Email allaqachon mavjud")
            user.email = data.email

        db.commit()
        db.refresh(user)
        return jsonable_encoder({
            "status": 200,
            "message": "Profile yangilandi",
            "username": user.username
        })
    except AuthJWTException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


