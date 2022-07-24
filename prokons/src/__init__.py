from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy import create_engine
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException, JWTDecodeError
from fastapi.responses import JSONResponse
from bcrypt import gensalt, hashpw, checkpw
from os import getenv
from dotenv import load_dotenv
from jwt.exceptions import DecodeError

load_dotenv()

engine = create_engine(f"{getenv('ENGINE')}://{getenv('USER')}@{getenv('HOST')}:{getenv('PORT')}/{getenv('DB')}")

Base = declarative_base()

session = sessionmaker(autocommit=False, bind=engine)

salt = gensalt()


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


class Setting(BaseModel):
    authjwt_secret_key: str = getenv("JWT_SECRET_KEY")


@AuthJWT.load_config
def get_config():
    return Setting()
