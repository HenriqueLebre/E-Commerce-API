# app/routers/order_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_user
from app.models.user_models import User
from app.schemas.order_schema import OrderResponse
from app.services.order_service import create_order, get_orders, get_order_by_id

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@router.post("/checkout", response_model=OrderResponse)
def checkout(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        return create_order(db, current_user.id)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))

@router.get("/", response_model=list[OrderResponse])
def list_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_orders(db, current_user.id)

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        return get_order_by_id(db, current_user.id, order_id)
    except ValueError as err:
        raise HTTPException(status_code=404, detail=str(err))