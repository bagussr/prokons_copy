from turtle import color
from fastapi import APIRouter, Depends, HTTPException, status
from src.__init__ import Session, get_db, JSONResponse
from src.handler.color import get_all_color, add_new_color, delete_color
from src.schemas.main import CreateColor

route = APIRouter(prefix="/color", tags=["color"])


@route.get("/")
def all_color(db: Session = Depends(get_db)):
    colors = get_all_color(db)
    if colors:
        data: list = []
        for x in colors:
            data.append({"id": x.id, "color": x.name})
        return data
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@route.post("/")
async def add_Color(db: Session = Depends(get_db), color: CreateColor = None):
    _color = await add_new_color(db, color)
    if _color:
        return JSONResponse({"msg": "color add", "data": {"color": _color.name}}, 201)
    raise HTTPException(status.HTTP_400_BAD_REQUEST)


@route.delete("/{id}")
def delete_color_(id: int, db: Session = Depends(get_db)):
    color = delete_color(db, id)
    return JSONResponse({"msg": "color deleted", "color": color.name}, 200)
