from src.__init__ import Session
from src.schemas.main import CreateVariant
from src.model.main import Variant


async def create_new_variant(db: Session, item: CreateVariant):
    variant = Variant(
        product_id=item.product_id,
        color_id=item.color_id,
        size=item.size,
        stock=item.stock,
        price=item.price,
        updated_at=item.updated_at,
    )
    db.add(variant)
    db.commit()
    db.refresh(variant)
    return variant


def get_all_variant(db: Session):
    variant = db.query(Variant).all()
    return variant


def get_variant_by_id(db: Session, id: int):
    variant = db.query(Variant).filter(Variant.id == id).first()
    return variant


def delete_variant_by_id(db: Session, id: int):
    variant = db.query(Variant).filter(Variant.id == id).first()
    db.delete(variant)
    db.commit()
    return variant


async def update_variant_by_id(db: Session, item: CreateVariant, id: int):
    variant = db.query(Variant).filter(Variant.id == id).first()
    if item.color_id:
        variant.color_id = item.color_id
    if item.size:
        variant.size = item.size
    if item.price:
        variant.price = item.price
    if item.stock:
        variant.stock = item.stock
    db.commit()
    db.refresh(variant)
    return variant


async def decrease_order(db: Session, id: int, qty: int):
    variant = get_variant_by_id(db, id)
    variant.stock = variant.stock - qty
    db.commit()
    db.refresh(variant)


def check_variant(db: Session, id: int):
    if get_variant_by_id(db, id):
        return True
    return False
