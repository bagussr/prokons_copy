# import all package install
from fastapi import FastAPI, HTTPException, status, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth.exceptions import AuthJWTException
from starlette.middleware.sessions import SessionMiddleware
import uvicorn

# imoprt package from local
from src.__init__ import Base, engine, get_db, Session, getenv, load_dotenv, session
from src.endpoins import user, product, variant, color, order, detail_order
from src.handler.user import check_admin
from src.handler.utils import create_admin
from src.model.main import User

# load .env file
load_dotenv()

# declare main application
app = FastAPI(title="azura_api_copy")

# add middleware for session
# add CORSMiddleware for cors
app.add_middleware(SessionMiddleware, secret_key=getenv("SECRET_KEY"))
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# add static file for image
app.mount("/public", StaticFiles(directory="prokons/public"), name="public")


# include all router from another application router
app.include_router(user.route)
app.include_router(product.route)
app.include_router(variant.route)
app.include_router(color.route)
app.include_router(order.route)
app.include_router(detail_order.route)

# create all table from model
Base.metadata.create_all(engine)
