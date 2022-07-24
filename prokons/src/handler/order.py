from typing import List
from src import Session
from src.schemas.main import CraeteOrder, CreateTransaction
from src.model.main import Order, Transaction
from src.handler.variant import decrease_order


async def create_order(db: Session, item: CraeteOrder):
    order = Order(
        transaction_id=item.transaction_id,
        variant_id=item.variant_id,
        qty=item.qty,
        total=item.total,
        updated_at=item.updated_at,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def get_order_by_id(db: Session, id: int):
    order = db.query(Order).filter(Order.id == id).first()
    return order


def get_all_order(db: Session):
    order = db.query(Order).all()
    return order


async def create_trasaction(db: Session, item: CreateTransaction):
    transaction = Transaction(user_id=item.user_id, status=item.status._value_, updated_at=item.updated_at)
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


async def update_transaction(db: Session, status: str, id: int):
    transaction = db.query(Transaction).filter(Transaction.id == id).first()
    transaction.status = status
    db.commit()
    db.refresh(transaction)
    return transaction
