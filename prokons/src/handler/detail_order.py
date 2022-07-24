from src import Session
from src.schemas.main import CreateLogOrder
from src.model.main import LogOrder


async def create_log_order(db: Session, item: CreateLogOrder):
    log_order = LogOrder(
        transaction_id=item.transaction_id, qty_total=item.qty_total, total=item.total, updated_at=item.updated_at
    )
    db.add(log_order)
    db.commit()
    db.refresh(log_order)
    return log_order


def get_log(db: Session):
    log_order = db.query(LogOrder).all()
    return log_order


def get_log_by_id(db: Session, id: int):
    log_order = db.query(LogOrder).filter(LogOrder.id == id).first()
    return log_order
