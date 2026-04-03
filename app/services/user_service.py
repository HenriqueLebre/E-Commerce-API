# app/services/user_service.py

from sqlalchemy.orm import Session
from app.models.user_models import User
from app.schemas.user_schema import UserUpdate
from app.core.security import hash_password


# ========== PRÓPRIO USUÁRIO ==========

def get_my_profile(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")
    return user


def update_my_profile(db: Session, user_id: int, data: UserUpdate) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")

    update_data = data.model_dump(exclude_unset=True)

    # Se mudou a senha, faz o hash
    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


# ========== ADMIN ==========

def get_all_users(db: Session) -> list[User]:
    return db.query(User).all()


def get_user_by_id(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")
    return user


def deactivate_user(db: Session, user_id: int) -> User:
    """Soft delete — desativa o usuário"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")
    if not user.active:
        raise ValueError("User already deactivated")

    user.active = False
    db.commit()
    db.refresh(user)
    return user