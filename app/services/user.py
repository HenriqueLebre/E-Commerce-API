from sqlalchemy.orm import Session
from app.models.user import User
import bycrypt

def validate_user(db: Session, data: UserCreate):
    existing =  db.query(User).filter(User.email == data.email).first()
    if existing:
        raise ValueError("Email already exists")
    
    number_existing = db.query(User).filter(User.number == data.number).first()
    if number_existing:
        raise ValueError("Number already exists")
    if len(data.number) < 10:
        raise ValueError("Number must be at least 10 characters long")

    password = data.password
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")
    if not any(char.isdigit() for char in password):
        raise ValueError("Password must contain at least one digit")
    if not any(char.isalpha() for char in password):
        raise ValueError("Password must contain at least one letter")
    
    password = bycrypt.hashpw(password.encode('utf-8'), bycrypt.gensalt())

    new_user = User(
        email=data.email,
        name=data.name,
        number=data.number,
        password=password.decode('utf-8')
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user