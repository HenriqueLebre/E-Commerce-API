from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_user, get_current_admin
from app.models.user_models import User
from app.models.order_models import Order
from app.schemas.order_schema import OrderResponse, CheckoutResponse
from app.services.order_service import create_order, get_orders, get_order_by_id

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/checkout", response_model=CheckoutResponse)
def checkout(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_order(db, current_user.id)

@router.get("/", response_model=list[OrderResponse])
def list_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_orders(db, current_user.id)

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_order_by_id(db, current_user.id, order_id)

@router.get("/admin/all", response_model=list[OrderResponse])
def list_all_orders(db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    return db.query(Order).all()