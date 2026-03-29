from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.models.user_models import User
from app.schemas.user_schema import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_user(db: Session, data: UserCreate) -> User:
    # Validação de email duplicado
    if db.query(User).filter(User.email == data.email).first():
        raise ValueError("Email already exists")

    # Validação de número duplicado
    if db.query(User).filter(User.number == data.number).first():
        raise ValueError("Number already exists")

    # Criar usuário com senha hasheada via passlib (não bcrypt direto)
    new_user = User(
        name=data.name,
        email=data.email,
        hashed_password=hash_password(data.password),  # ← usa a função que já existe
        number=data.number,
        active=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(db: Session, email: str, password: str) -> User:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user