from src.__init__ import Session
from src.model.main import User
from src.schemas.main import CreateUser
from .utils import create_password

# function to create new user
async def create_user(db: Session, user: CreateUser):
    password = create_password(user.password.encode("utf-8"))
    _user = User(
        name=user.name, username=user.username, password=password, is_admin=user.is_admin, updated_at=user.updated_at
    )
    db.add(_user)
    db.commit()
    db.refresh(_user)
    return _user


# function to get user by username
def get_user_by_username(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    return user


# function to get user by id
def get_user_by_id(db: Session, id: int):
    user = db.query(User).filter(User.id == id).first()
    return user


# function to get all user
def all_user(db: Session):
    user = db.query(User).all()
    return user


# function to delete user
def delete_user(db: Session, id: int):
    user = db.query(User).filter(User.id == int).first()
    db.delete(user)
    db.commit()
    return user


# function to upddate user
async def update_user(db: Session, item: CreateUser, id: int):
    user = db.query(User).filter(User.id == id).first()
    user.name = item.name
    user.username = item.username
    if item.password:
        user.password = create_password(item.password.encode("utf-8"))
    user.updated_at = item.updated_at
    user.is_admin = item.is_admin
    db.commit()
    db.refresh(user)
    return user


# function to check admin
def check_admin(db: Session):
    return db.query(User).filter(User.is_admin == True).all()
