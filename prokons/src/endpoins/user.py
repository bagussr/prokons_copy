from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Body
from src.schemas.main import CreateUser
from src.__init__ import Session, get_db, JSONResponse, AuthJWT, DecodeError
from src.handler.user import create_user, get_user_by_username, delete_user, update_user, all_user, get_user_by_id
from src.handler.utils import check_password

route = APIRouter(prefix="/user", tags=["user"])


@route.get("/")
def get_user(db: Session = Depends(get_db)):
    user = all_user(db)
    if user:
        data: list = []
        for x in user:
            data.append({"id": x.id, "name": x.name, "username": x.username, "admin": x.is_admin})
        return JSONResponse({"msg": "success", "data": data})
    raise HTTPException(404, {"msg": "not found"})


@route.get("/{id}")
def get_by_id(id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, id)
    if user:
        return JSONResponse(
            {
                "msg": "success",
                "data": {"id": user.id, "name": user.name, "username": user.username, "admin": user.is_admin},
            }
        )


@route.post("/", response_model=CreateUser)
async def create_user_new(_user: CreateUser, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    try:
        user = await create_user(db, _user)
        data: dict = {"name": user.name, "username": user.username}
        return JSONResponse({"msg": "User Created", "data": data}, status_code=201)
    except DecodeError:
        return HTTPException(
            status_code=status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED, detail={"msg": "not authenticated"}
        )


@route.post("/login")
async def login(req: Any = Body(...), auth: AuthJWT = Depends(), db: Session = Depends(get_db)):
    _user = get_user_by_username(db, req["username"])
    if _user is None:
        raise HTTPException(404, "Username Tidak ditemukan")
    if check_password(db, req["username"], req["password"]) is False:
        raise HTTPException(404, "Password anda salah")
    token = auth.create_access_token(subject=_user.username, expires_time=False)
    return JSONResponse({"msg": "Login Success", "token": token}, status_code=200)


@route.delete("/{id}")
def delete_(id: int, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    auth.jwt_required()
    delete_user(db, id)
    return JSONResponse({"msg": "Delete Success"}, status.HTTP_200_OK)


@route.put("/{id}")
async def update_(id: int, _user: CreateUser, db: Session = Depends(get_db)):
    user = await update_user(db, _user, id)
    data: dict = {"name": user.name, "username": user.username}
    return JSONResponse({"msg": "Update Success", "data": data}, status.HTTP_200_OK)
