from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey, Enum, func, event
import enum

from src.__init__ import Base, relationship, engine


class Status(enum.Enum):
    process: str = "process"
    paid: str = "paid"


class User(Base):
    __tablename__ = "user_prokons"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    username = Column(String(50), unique=True)
    password = Column(String(255))
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, nullable=True)

    user_id = relationship("Transaction", back_populates=("user"))

    def __repr__(self) -> str:
        return f"user : name  = {self.name}, username ={self.username}"


class Color(Base):
    __tablename__ = "colors"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, nullable=True)

    color_owner = relationship("Variant", back_populates="variant_color")

    def __repr__(self) -> str:
        return f"{self.name}"


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    image_path = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, nullable=True)

    variants = relationship("Variant", back_populates="owner")

    def __repr__(self) -> str:
        return f"user:{self.name}, {self.image_path}"


class Variant(Base):
    __tablename__ = "variant"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    color_id = Column(Integer, ForeignKey("colors.id"))
    size = Column(String(50))
    price = Column(Integer)
    stock = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, nullable=True)

    owner = relationship("Product", back_populates="variants")
    variant = relationship("Order", back_populates="owner")
    variant_color = relationship("Color", back_populates="color_owner")

    def __repr__(self) -> str:
        return f"user:{self.id}, {self.price}, {self.stock}"


class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer, ForeignKey("transaction.id"))
    variant_id = Column(Integer, ForeignKey("variant.id"))
    qty = Column(Integer)
    total = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, nullable=True)

    owner = relationship("Variant", back_populates="variant")
    transaction = relationship("Transaction", back_populates="owner")

    def __repr__(self) -> str:
        return f"order:{self.id}, qty: {self.qty},total: {self.total}"


class Transaction(Base):
    __tablename__ = "transaction"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user_prokons.id"))
    status = Column(Enum(Status))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, nullable=True)

    owner = relationship("Order", back_populates="transaction")
    user = relationship("User", back_populates="user_id")
    log_order = relationship("LogOrder", back_populates="owner")

    def __repr__(self) -> str:
        return f"user:{self.id}, {self.status}"


class LogOrder(Base):
    __tablename__ = "log_order"
    id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer, ForeignKey("transaction.id"))
    qty_total = Column(Integer)
    total = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, nullable=True)

    owner = relationship("Transaction", back_populates="log_order")

    def __repr__(self) -> str:
        return f"user:{self.id}, {self.qty}, {self.total}"


Base.metadata.create_all(engine)
