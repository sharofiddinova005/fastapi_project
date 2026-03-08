from fastapi import FastAPI
from database import engine, Base
from product_router import router
from auth_router import auth_
from fastapi_jwt_auth import AuthJWT
from schemas import Settings

@AuthJWT.load_config
def get_config():
    return Settings()

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(router, prefix="/product")
app.include_router(auth_, prefix="/auth")

