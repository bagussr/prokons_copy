from fastapi import FastAPI, HTTPException, status, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth.exceptions import AuthJWTException
from starlette.middleware.sessions import SessionMiddleware
import uvicorn

from src.__init__ import Base, engine, get_db, Session, getenv, load_dotenv, session
from src.endpoins import user, product, variant, color, order, detail_order
from src.handler.user import check_admin
from src.handler.utils import create_admin
from src.model.main import User

load_dotenv()


app = FastAPI(title="azura_api_copy")

app.add_middleware(SessionMiddleware, secret_key=getenv("SECRET_KEY"))
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/public", StaticFiles(directory="prokons/public"), name="public")

app.include_router(user.route)
app.include_router(product.route)
app.include_router(variant.route)
app.include_router(color.route)
app.include_router(order.route)
app.include_router(detail_order.route)

Base.metadata.create_all(engine)
