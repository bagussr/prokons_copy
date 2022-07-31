from pydantic import BaseModel
from typing import Any, Optional, Union
from enum import Enum
from datetime import datetime


class Status(Enum):
    process: str = "process"
    paid: str = "paid"


class Category(Enum):
    shirt: str = "Shirt"
    pant: str = "Pant"
    suit: str = "Suite"


class UserSchemas(BaseModel):
    name: str
    username: str
    password: Optional[str]
    is_admin: bool = False
    updated_at: Union[datetime, Any] = datetime.now()


class CreateUser(UserSchemas):
    pass

    class config:
        orm_mode = True


class ColorSchemas(BaseModel):
    name: str
    updated_at: Union[datetime, Any] = datetime.now()


class CreateColor(ColorSchemas):
    pass

    class config:
        orm_mode = True


class ProductSchemas(BaseModel):
    name: str
    updated_at: Union[datetime, Any] = datetime.now()


class CreateProduct(ProductSchemas):
    pass

    class config:
        orm_mode = True


class VariantSchemas(BaseModel):
    product_id: Optional[int]
    color_id: Optional[int]
    category: Optional[Category]
    size: Optional[str]
    stock: Optional[int]
    price: Optional[int]
    updated_at: Union[datetime, Any] = datetime.now()


class CreateVariant(VariantSchemas):
    pass

    class config:
        orm_mode = True


class OrderSchemas(BaseModel):
    transaction_id: Optional[int]
    variant_id: int
    qty: int
    total: int
    updated_at: Union[datetime, Any] = datetime.now()


class CraeteOrder(OrderSchemas):
    pass

    class config:
        orm_mode = True


class TrasactionSchemas(BaseModel):
    user_id: int
    status: Status
    updated_at: Union[datetime, Any] = datetime.now()


class CreateTransaction(TrasactionSchemas):
    pass

    class config:
        orm_mode = True
        use_enum_values = True


class LogOrderSchemas(BaseModel):
    transaction_id: int
    qty_total: int
    total: int
    updated_at: Union[datetime, Any] = datetime.now()


class CreateLogOrder(LogOrderSchemas):
    pass

    class config:
        orm_mode = True
        use_enum_values = True
