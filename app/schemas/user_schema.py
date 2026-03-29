from pydantic import BaseModel, EmailStr
from datetime import datetime

#Schema for user creation - Entrada
class UserBase(BaseModel):
    email: EmailStr
    name: str
    number: str

@field_validator('number')
@classmethod
def validate_number(cls, value):
    if len(value) < 0 or len(value) > 15:
        raise ValueError('Number must be between 1 and 15 characters long')
    return value


class UserCreate(UserBase):
    password: str
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(char.isdigit() for char in value):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isalpha() for char in value):
            raise ValueError('Password must contain at least one letter')
        return value

#Schema for user creation - Saida
class UserResponse(UserBase):
    id: int
    active: bool
    datecreation: datetime

    class Config:
        from_attributes = True