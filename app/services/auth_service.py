from sqlalchemy.orm import Session
from app.models.user_models import User
from app.schemas.user_schema import UserCreate
from app.core.security import hash_password, verify_password
from app.core.exceptions import ConflictException

def create_user(db: Session, data: UserCreate) -> User:
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise ConflictException("Email already registered")

    user = User(
        email=data.email,
        name=data.name,
        number=data.number,
        password=hash_password(data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        return None
    return user