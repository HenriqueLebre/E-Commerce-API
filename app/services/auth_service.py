from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.models.user import User
from app.schemas.user import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_user(db: Session, dados: UserCreate) -> User:
    existing = db.query(User).filter(
        User.email == dados.email
    ).first()
    if existing:
        raise ValueError("Email já cadastrado")

    hashed_password = hash_password(dados.password)

    novo = User(
        name = dados.name,
        email=dados.email,
        hashed_password=hashed_password,
        number=dados.number,
        active=True
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)

    return novo

def authenticate_user(db: Session, email: str, password: str) -> User:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user;