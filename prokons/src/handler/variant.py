from src.__init__ import Session
from src.schemas.main import CreateVariant
from src.model.main import Variant

# function to create new variant
async def create_new_variant(db: Session, item: CreateVariant):
    variant = Variant(
        product_id=item.product_id,
        color_id=item.color_id,
        category=item.category,
        size=item.size,
        stock=item.stock,
        price=item.price,
        updated_at=item.updated_at,
    )
    db.add(variant)
    db.commit()
    db.refresh(variant)
    return variant


# function to get all variant
def get_all_variant(db: Session):
    variant = db.query(Variant).all()
    return variant


# function to get variant by id
def get_variant_by_id(db: Session, id: int):
    variant = db.query(Variant).filter(Variant.id == id).first()
    return variant


# function to delete variant
def delete_variant_by_id(db: Session, id: int):
    variant = db.query(Variant).filter(Variant.id == id).first()
    db.delete(variant)
    db.commit()
    return variant


# function to update variant
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
    if item.category:
        variant.category = item.category
    db.commit()
    db.refresh(variant)
    return variant


# function to trigger add order
async def decrease_order(db: Session, id: int, qty: int):
    variant = get_variant_by_id(db, id)
    variant.stock = variant.stock - qty
    db.commit()
    db.refresh(variant)


# fucntion to check variant
def check_variant(db: Session, id: int):
    if get_variant_by_id(db, id):
        return True
    return False
