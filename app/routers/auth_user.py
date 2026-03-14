from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.auth_service import create_user
from app.schemas.user import UserCreate, UserResponse
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