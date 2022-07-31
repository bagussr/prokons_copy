from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Body
from src.schemas.main import CreateUser
from src.__init__ import Session, get_db, JSONResponse, AuthJWT, DecodeError
from src.handler.user import create_user, get_user_by_username, delete_user, update_user, all_user, get_user_by_id
from src.handler.utils import check_password, check_authrize

route = APIRouter(prefix="/user", tags=["user"])

# define variable for denylist for development or use redist for production
denylist: set = set()

# revoke access token
@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decrypted_token):
    jti = decrypted_token["jti"]
    return jti in denylist


# endpoint to get all user
@route.get("/", dependencies=[Depends(check_authrize)])
def get_user(db: Session = Depends(get_db)):
    user = all_user(db)
    if user:
        data: list = []
        for x in user:
            data.append({"Id": x.id, "Name": x.name, "Username": x.username, "Admin": x.is_admin})
        return JSONResponse({"msg": "success", "data": data})
    raise HTTPException(404, {"msg": "not found"})


# endpoint for get user by id
@route.get("/{id}", dependencies=[Depends(check_authrize)])
def get_by_id(id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, id)
    if user:
        return JSONResponse(
            {
                "msg": "success",
                "data": {"id": user.id, "name": user.name, "username": user.username, "admin": user.is_admin},
            }
        )


# endpoint for create new user
@route.post("/", response_model=CreateUser, dependencies=[Depends(check_authrize)])
async def create_user_new(_user: CreateUser, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    try:
        user = await create_user(db, _user)
        data: dict = {"name": user.name, "username": user.username}
        return JSONResponse({"msg": "User Created", "data": data}, status_code=201)
    except DecodeError:
        return HTTPException(
            status_code=status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED, detail={"msg": "not authenticated"}
        )


# endpoint to get login
@route.post("/login")
async def login(req: Any = Body(...), auth: AuthJWT = Depends(), db: Session = Depends(get_db)):
    _user = get_user_by_username(db, req["username"])
    if _user is None:
        raise HTTPException(404, "Username Tidak ditemukan")
    if check_password(db, req["username"], req["password"]) is False:
        raise HTTPException(404, "Password anda salah")
    token = auth.create_access_token(subject=_user.username, expires_time=False)
    return JSONResponse({"msg": "Login Success", "token": token}, status_code=200)


# endpoint to delete user
@route.delete("/delete/{id}", dependencies=[Depends(check_authrize)])
def delete_(id: int, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    auth.jwt_required()
    delete_user(db, id)
    return JSONResponse({"msg": "Delete Success"}, status.HTTP_200_OK)


# enpoint to update user
@route.put("/{id}", dependencies=[Depends(check_authrize)])
async def update_(id: int, _user: CreateUser, db: Session = Depends(get_db)):
    user = await update_user(db, _user, id)
    data: dict = {"name": user.name, "username": user.username}
    return JSONResponse({"msg": "Update Success", "data": data}, status.HTTP_200_OK)


# endpoint to logout
@route.delete("/logout", dependencies=[Depends(check_authrize)])
def logout(auth: AuthJWT = Depends()):
    jti = auth.get_raw_jwt()["jti"]
    denylist.add(jti)
    return JSONResponse(status_code=200, content={"msg": "logout success"})
