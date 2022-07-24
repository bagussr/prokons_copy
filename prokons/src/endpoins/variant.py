from fastapi import APIRouter, Depends, HTTPException
from src.schemas.main import CreateVariant
from src import get_db, JSONResponse
from src.handler.variant import *
from src.handler.utils import product_variant


route = APIRouter(prefix="/variant", tags=["variant"])


@route.get("/")
def get_variant_all(db: Session = Depends(get_db)):
    variant = get_all_variant(db)
    if variant:
        data: list = []
        for x in variant:
            data.append(
                {
                    "id": x.id,
                    "product_id": x.product_id,
                    "color": x.color_id,
                    "size": x.size,
                    "price": x.price,
                    "stock": x.stock,
                }
            )
        return JSONResponse({"msg": "success", "data": data}, 200)
    raise HTTPException(404, {"msg": "not found"})


@route.get("/products")
async def get_all_product_variant(db: Session = Depends(get_db)):
    products = await product_variant(db)
    if products:
        data: list = []
        for x in products:
            data.append(x)
        return JSONResponse({"msg": "success", "data": data})
    raise HTTPException(404, {"msg": "not found"})


@route.post("/")
async def add_variant(item: CreateVariant, db: Session = Depends(get_db)):
    variant = await create_new_variant(db, item)
    data: dict = {
        "id": variant.id,
        "product_id": variant.product_id,
        "color": variant.color_id,
        "size": variant.size,
        "price": variant.price,
        "stock": variant.stock,
    }
    return JSONResponse({"msg": "variant created", "data": data}, 201)


@route.delete("/{id}")
def delete_variant(id: int, db: Session = Depends(get_db)):
    _variant = get_variant_by_id(db, id)
    if _variant:
        delete_variant_by_id(db, id)
        return JSONResponse({"msg": "variant deleted", "data": {"variant_id": _variant.id}})
    raise HTTPException(404, {"msg": "not found"})


@route.put("/{id}")
async def updaet_variant(item: CreateVariant, id: int, db: Session = Depends(get_db)):
    _variant = get_variant_by_id(db, id)
    if _variant:
        variant = await update_variant_by_id(db, item, id)
        data: dict = {
            "id": variant.id,
            "product_id": variant.product_id,
            "color": variant.color_id,
            "size": variant.size,
            "price": variant.price,
            "stock": variant.stock,
        }
        return JSONResponse({"msg": "variant updated", "data": data})
    raise HTTPException(404, {"msg": "not found"})
