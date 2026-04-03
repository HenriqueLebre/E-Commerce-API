from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    name: str
    number: str

    @field_validator("number")
    @classmethod
    def validate_number(cls, value):
        if value is not None:
            if len(value) < 1 or len(value) > 15:
                raise ValueError("Number must be between 1 and 15 characters")
        return value

class UserCreate(UserBase):
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isalpha() for char in value):
            raise ValueError("Password must contain at least one letter")
        return value

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    number: Optional[str] = None
    password: Optional[str] = None

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if value is not None:
            if len(value) < 8:
                raise ValueError("Password must be at least 8 characters")
            if not any(char.isdigit() for char in value):
                raise ValueError("Password must contain at least one digit")
            if not any(char.isalpha() for char in value):
                raise ValueError("Password must contain at least one letter")
        return value

    @field_validator("number")
    @classmethod
    def validate_number(cls, value):
        if value is not None:
            if len(value) < 1 or len(value) > 15:
                raise ValueError("Number must be between 1 and 15 characters")
        return value

class UserResponse(UserBase):
    id: int
    active: bool
    datecreation: datetime

    class Config:
        from_attributes = True