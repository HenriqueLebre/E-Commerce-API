from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.auth_service import authenticate_user, create_user
from app.schemas.user_schema import UserCreate, UserResponse
from app.schemas.token_schema import TokenResponse, LoginRequest
from app.core.security import create_access_token
from app.database import get_db

router = APIRouter(
    prefix="/auth",      
    tags=["Auth"]        
)

@router.post("/register", response_model = UserResponse)    # → POST /auth/register
def register(dados: UserCreate, db: Session = Depends(get_db)):
    try:
        user = create_user(db, dados)
        return user
    except ValueError as err:
        raise HTTPException(status_code=409, detail=str(err))
    
@router.post("/login", response_model=TokenResponse)       # → POST /auth/login
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.email, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token = create_access_token({"sub": user.email})
    return TokenResponse(access_token=token, token_type="bearer");