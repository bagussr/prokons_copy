from typing import List
from fastapi import APIRouter, Depends, HTTPException
from jwt import DecodeError
from src import get_db, Session, JSONResponse, AuthJWT, AuthJWTException, JWTDecodeError
from src.handler.order import get_all_order, get_order_by_id, create_order, create_trasaction, update_transaction
from src.handler.user import get_user_by_username
from src.handler.detail_order import create_log_order
from src.handler.variant import decrease_order, check_variant
from src.schemas.main import CraeteOrder, CreateTransaction, CreateLogOrder

route = APIRouter(prefix="/order", tags=["order"])


@route.get("/")
def get_order(db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    try:
        auth.jwt_required()
        order = get_all_order(db)
        if order:
            data: list = []
            for x in order:
                data.append(
                    {
                        "id": x.id,
                        "trasaction_id": x.transaction_id,
                        "variant_id": x.variant_id,
                        "qty": x.qty,
                        "total": x.total,
                    }
                )
            return JSONResponse({"msg": "success", "data": data})
        raise HTTPException(404, {"msg": "not found"})
    except DecodeError:
        raise AuthJWTException


@route.get("/{id}")
def order_by_id(id: int, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    try:
        auth.jwt_required()
        order = get_order_by_id(db, id)
        if order:
            data: dict = {
                "id": order.id,
                "trasaction_id": order.transaction_id,
                "variant_id": order.variant_id,
                "qty": order.qty,
                "total": order.total,
            }
            return JSONResponse({"msg": "success", "data": data})
        raise HTTPException(404, {"msg": "not found"})
    except DecodeError:
        raise AuthJWTException()


@route.post("/")
async def add_order(item: List[CraeteOrder], db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    total: int = 0
    qty_total: int = 0
    try:
        auth.jwt_required()
        current_user = auth.get_jwt_subject()
        user = get_user_by_username(db, current_user)
        try:
            transaction = await create_trasaction(db, CreateTransaction(user_id=user.id, status="process"))
            for x in item:
                if not check_variant(db, x.variant_id):
                    raise HTTPException(404, {"msg": "not found"})
                total += x.total
                qty_total += x.qty
                x.transaction_id = transaction.id
                await decrease_order(db, x.variant_id, x.qty)
                order = await create_order(db, x)
            await update_transaction(db, "paid", transaction.id)
            await create_log_order(db, CreateLogOrder(transaction_id=transaction.id, qty_total=qty_total, total=total))
        except:
            raise HTTPException(400, {"msg": "bad request"})
        if order:
            return JSONResponse({"msg": "success", "trasaction_id": transaction.id})
        raise HTTPException(404, {"msg": "not found"})
    except JWTDecodeError:
        raise AuthJWTException()
