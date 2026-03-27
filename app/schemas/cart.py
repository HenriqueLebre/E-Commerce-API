from pydantic import BaseModel, field_validator
from typing import Optional

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, value):
        if value < 1:
            raise ValueError("Quantity must be at least 1")
        return value

class CartItemUpdate(BaseModel):
    quantity: int

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, value):
        if value < 1:
            raise ValueError("Quantity must be at least 1")
        return value

class CartItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    product_name: Optional[str] = None
    product_price: Optional[float] = None

    class Config:
        from_attributes = True

class CartResponse(BaseModel):
    id: int
    items: list[CartItemResponse]
    total: float

    class Config:
        from_attributes = True