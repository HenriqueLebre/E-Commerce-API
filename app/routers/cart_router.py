from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.cart import CartItemCreate, CartItemUpdate, CartResponse
from app.services.cart_service import add_item, get_cart, update_item, remove_item, clear_cart

router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)

@router.get("/", response_model=CartResponse)
def view_cart(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_cart(db, current_user.id)

@router.post("/items", response_model=CartResponse)
def add_to_cart(data: CartItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        return add_item(db, current_user.id, data)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))

@router.put("/items/{item_id}", response_model=CartResponse)
def update_cart_item(item_id: int, data: CartItemUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        return update_item(db, current_user.id, item_id, data)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))

@router.delete("/items/{item_id}", response_model=CartResponse)
def remove_cart_item(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        return remove_item(db, current_user.id, item_id)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))

@router.delete("/")
def clear_all(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    clear_cart(db, current_user.id)
    return {"detail": "Cart cleared successfully"}