from datetime import datetime
from src.__init__ import salt, checkpw, hashpw, Session
from src.model.main import User, Variant, Product, Color


def create_password(passowrd: str):
    hashed_password = hashpw(passowrd, salt)
    return hashed_password


async def create_admin(db: Session):
    user = User(
        name="admin",
        username="admin",
        password=create_password("admin".encode("utf-8")),
        is_admin=True,
        updated_at=datetime.now(),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def check_password(db: Session, username: str, password: str):
    _user = db.query(User).filter(User.username == username).first()
    return checkpw(password.encode("utf-8"), _user.password.encode("utf-8"))


async def product_variant(db: Session):
    product = db.query(Product).all()
    data: list = []
    for x in product:
        variant = db.query(Variant).filter(Variant.product_id == x.id).all()
        variants: list = []
        for y in variant:
            color = db.query(Color).filter(Color.id == y.color_id).first()
            variants.append(
                {"variant_id": y.id, "color": color.name, "size": y.size, "price": y.price, "stock": y.stock}
            )
        data.append({"id": x.id, "name": x.name, "image_path": x.image_path, "variant": variants})
    return data
