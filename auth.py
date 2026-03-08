from sqlalchemy.orm import Session
from models import User
from schemas import SignUpSchema
from fastapi import HTTPException, status
from sqlalchemy import or_
from werkzeug.security import generate_password_hash
from fastapi.encoders import jsonable_encoder


def signup(db: Session, data: SignUpSchema):

    db_user = db.query(User).filter(
        or_(User.username == data.username, User.email == data.email)
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


