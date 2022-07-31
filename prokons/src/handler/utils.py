from datetime import datetime
from src.__init__ import salt, checkpw, hashpw, Session, AuthJWT, JWTDecodeError
from src.model.main import User, Variant, Product, Color
from fastapi import Depends

# function for create hash password
def create_password(passowrd: str):
    hashed_password = hashpw(passowrd, salt)
    return hashed_password


# function to create admin
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


# function to check input password and hashed password
def check_password(db: Session, username: str, password: str):
    _user = db.query(User).filter(User.username == username).first()
    return checkpw(password.encode("utf-8"), _user.password.encode("utf-8"))


# function to get all product with variants
async def product_variant(db: Session):
    product = db.query(Product).all()
    data: list = []
    for x in product:
        variant = db.query(Variant).filter(Variant.product_id == x.id).all()
        variants: list = []
        for y in variant:
            color = db.query(Color).filter(Color.id == y.color_id).first()
            variants.append(
                {
                    "Id": y.id,
                    "Category": y.category,
                    "Color": color.name,
                    "Size": y.size,
                    "Price": y.price,
                    "Stock": y.stock,
                }
            )
        data.append({"IId": x.id, "Name": x.name, "Image": x.image_path, "Variant": variants})
    return data


# dependency to check authorize
def check_authrize(auth: AuthJWT = Depends()):
    try:
        auth.jwt_required()
        pass
    except JWTDecodeError:
        raise {"msg": "not authenticated"}
