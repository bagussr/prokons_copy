from datetime import datetime
from turtle import update
from typing import Optional
from src import Session
from src.model.main import Product
from src.schemas.main import CreateProduct

# function to create new product
async def create_new_product(db: Session, name: str, path: str):
    file = Product(name=name, image_path=path, updated_at=datetime.now())
    db.add(file)
    db.commit()
    db.refresh(file)
    return file


# function to get all product
def get_all_product(db: Session):
    product = db.query(Product).all()
    return product


# function to get product by id
def get_product_by_id(db: Session, id: int):
    product = db.query(Product).filter(Product.id == id).first()
    return product


# function to detele product
def delete_product(db: Session, id: int):
    product = db.query(Product).filter(Product.id == id).first()
    db.delete(product)
    db.commit()
    return product


# function to update product
async def update_product(db: Session, name: str, id: int, path: Optional[str] = None):
    product = db.query(Product).filter(Product.id == id).first()
    product.name = name
    if path is not None:
        product.image_path = path
    db.commit()
    db.refresh(product)
    return product
