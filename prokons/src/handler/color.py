from src.__init__ import Session
from src.model.main import Color
from src.schemas.main import CreateColor


def get_all_color(db: Session):
    color = db.query(Color).all()
    return color


async def add_new_color(db: Session, _color=CreateColor):
    color = Color(name=_color.name, updated_at=_color.updated_at)
    db.add(color)
    db.commit()
    db.refresh(color)
    return color


def delete_color(db: Session, id: int):
    color = db.query(Color).filter(Color.id == id).first()
    db.delete(color)
    db.commit()
    return color
