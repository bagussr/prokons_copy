from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime

from src import Session, get_db, AuthJWT, AuthJWTException, JWTDecodeError, JSONResponse
from src.handler.detail_order import get_log, get_log_by_id

route = APIRouter(prefix="/log-order", tags=["log_order"])


@route.get("/")
def get_detail_order(db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    data: list = []
    try:
        auth.jwt_required()
        log = get_log(db)
        for x in log:
            data.append(
                {
                    "id": x.id,
                    "transaction_id": x.transaction_id,
                    "qty_total": x.qty_total,
                    "total": x.total,
                    "order_create": str(x.created_at),
                }
            )
        return JSONResponse({"msg": "success", "data": data})
    except JWTDecodeError:
        raise AuthJWTException


@route.get("/{id}")
def get_transaction(id: int, db: Session = Depends(get_db), auth: AuthJWT = Depends()):
    try:
        auth.jwt_required()
        log = get_log_by_id(db, id)
        if not log:
            raise HTTPException(404, {"msg": "not found"})
        print(str(log.created_at))
        return JSONResponse(
            {
                "msg": "success",
                "data": {
                    "id": log.id,
                    "transaction_id": log.transaction_id,
                    "qty_total": log.qty_total,
                    "total": log.total,
                    "order_create": str(log.created_at),
                },
            }
        )
    except JWTDecodeError:
        raise AuthJWTException()
