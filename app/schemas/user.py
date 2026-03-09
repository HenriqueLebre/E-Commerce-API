from pydantic import BaseModel, EmailStr
from datetime import datetime

#Schema for user creation - Entrada
class UserBase(BaseModel):
    email: EmailStr
    name: str
    number: str

class UserCreate(UserBase):
    password: str

#Schema for user creation - Saida
class UserResponse(UserBase):
    id: int
    active: bool
    datecreation: datetime

    class Config:
        from_attributes = True