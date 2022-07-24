from datetime import datetime
from turtle import update
from typing import Optional
from src import Session
from src.model.main import Product
from src.schemas.main import CreateProduct


async def create_new_product(db: Session, name: str, path: str):
    file = Product(name=name, image_path=path, updated_at=datetime.now())
    db.add(file)
    db.commit()
    db.refresh(file)
    return file


def get_all_product(db: Session):
    product = db.query(Product).all()
    return product


def get_product_by_id(db: Session, id: int):
    product = db.query(Product).filter(Product.id == id).first()
    return product


def delete_product(db: Session, id: int):
    product = db.query(Product).filter(Product.id == id).first()
    db.delete(product)
    db.commit()
    return product


async def update_product(db: Session, name: str, id: int, path: Optional[str] = None):
    product = db.query(Product).filter(Product.id == id).first()
    product.name = name
    if path is not None:
        product.image_path = path
    db.commit()
    db.refresh(product)
    return product
