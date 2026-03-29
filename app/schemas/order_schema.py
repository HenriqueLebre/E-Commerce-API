from pydantic import BaseModel
from datetime import datetime

class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    status: str
    total: float
    datecreation: datetime
    items: list[OrderItemResponse]

    class Config:
        from_attributes = True