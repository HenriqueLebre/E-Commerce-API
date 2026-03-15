from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional

class ProductBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    category: Optional[str] = None
    image_url: Optional[str] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if value is not None:
            if len(value) < 2 or len(value) > 100:
                raise ValueError("Name must be between 2 and 100 characters")
        return value

    @field_validator("price")
    @classmethod
    def validate_price(cls, value):
        if value is not None and value <= 0:
            raise ValueError("Price must be greater than 0")
        return value

    @field_validator("stock")
    @classmethod
    def validate_stock(cls, value):
        if value is not None and value < 0:
            raise ValueError("Stock cannot be negative")
        return value

# Create — campos obrigatórios (sobrescreve os Optional)
class ProductCreate(ProductBase):
    name: str
    price: float
    stock: int

# Update — tudo Optional (herda do Base)
class ProductUpdate(ProductBase):
    pass

# Response
class ProductResponse(ProductBase):
    id: int
    name: str
    price: float
    stock: int
    active: bool
    datecreation: datetime
    dateupdated: Optional[datetime] = None
    datedeactivated: Optional[datetime] = None

    class Config:
        from_attributes = True