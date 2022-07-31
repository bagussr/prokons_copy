# import all package
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

# load .env file
load_dotenv()

# create engine for database
engine = create_engine(f"{getenv('ENGINE')}://{getenv('USER')}@{getenv('HOST')}:{getenv('PORT')}/{getenv('DB')}")

# create base for define model
Base = declarative_base()

# create session for database
session = sessionmaker(autocommit=False, bind=engine)

# create salt for hashing method
salt = gensalt()

# dependecy for use session database
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


# setting for authentication
class Setting(BaseModel):
    authjwt_secret_key: str = getenv("JWT_SECRET_KEY")
    authjwt_denylist_enabled: bool = True
    authjwt_denylist_token_checks: set = {"access"}


# load setting authentication
@AuthJWT.load_config
def get_config():
    return Setting()
