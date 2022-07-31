from typing import Optional
from fastapi import APIRouter, Body, File, Form, HTTPException, UploadFile, Depends
from src.schemas.main import CreateProduct
from src.handler.product import create_new_product, get_all_product, get_product_by_id, delete_product, update_product
from src.handler.utils import check_authrize
from src.__init__ import Session, get_db, JSONResponse
from pathlib import Path
from aiofiles import open
import os

x = Path("prokons/public/image").absolute()
y = Path("prokons").absolute()


route = APIRouter(prefix="/product", tags=["product"], dependencies=[Depends(check_authrize)])

# endpoint to create new product
@route.post("/")
async def add_product(name: str = Form(...), file: UploadFile = File(), db: Session = Depends(get_db)):
    try:
        async with open(os.path.join(x, file.filename), "wb") as r:
            content = await file.read()
            await file.close()
            await r.write(content)
    finally:
        product = await create_new_product(db, name, os.path.join("/public/image/", file.filename))
    data: dict = {"id": product.id, "name": product.name, "path": product.image_path}
    return JSONResponse({"msg": "update success", "data": data}, 201)


# endpoint to get all product
@route.get("/")
def get_product(db: Session = Depends(get_db)):
    product = get_all_product(db)

    if product:
        data: list = []
        for x in product:
            data.append({"id": x.id, "name": x.name, "path": x.image_path})
        return JSONResponse({"msg": "success", "data": data})
    raise HTTPException(404, detail={"msg": "not found"})


# endpoint to delete product
@route.delete("/{id}")
def delete_product_id(id: int, db: Session = Depends(get_db)):
    _product = get_product_by_id(db, id)
    if _product:
        product = delete_product(db, id)
        dir_file = Path("prokons/" + product.image_path).absolute()
        if os.path.isfile(dir_file):
            os.remove(dir_file)
        return JSONResponse({"msg": "delete Success"})
    raise HTTPException(404, detail={"msg": "not found"})


# endpoint to update product
@route.put("/{id}")
async def update_product_id(
    id: int, name=Body(), file: Optional[UploadFile] = File(None), db: Session = Depends(get_db)
):
    _product = get_product_by_id(db, id)
    if _product:
        if file is not None:
            dir_file = Path("prokons/" + _product.image_path).absolute()
            try:
                async with open(os.path.join(x, file.filename), "wb") as r:
                    content = await file.read()
                    await file.close()
                    await r.write(content)
            finally:
                if os.path.isfile(dir_file):
                    os.remove(dir_file)
                product = await update_product(db, name, id, os.path.join("/public/image/", file.filename))
                data: dict = {"id": product.id, "name": product.name, "path": product.image_path}
                return JSONResponse({"msg": "update success", "data": data}, 201)
        product = await update_product(db, name, id)
        data: dict = {"id": product.id, "name": product.name, "path": _product.image_path}
        return JSONResponse({"msg": "update success", "data": data}, 201)
    raise HTTPException(404, detail={"msg": "not found"})
