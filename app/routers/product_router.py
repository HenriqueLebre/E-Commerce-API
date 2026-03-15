# app/routers/product_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.services.product_service import (
    create_product, get_products, get_product_by_id, update_product, delete_product
)

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.post("/", response_model=ProductResponse)
def create(data: ProductCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.isadmin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return create_product(db, data)

@router.get("/", response_model=list[ProductResponse])
def list_all(db: Session = Depends(get_db)):
    return get_products(db)

@router.get("/{product_id}", response_model=ProductResponse)
def get_by_id(product_id: int, db: Session = Depends(get_db)):
    try:
        return get_product_by_id(db, product_id)
    except ValueError as err:
        raise HTTPException(status_code=404, detail=str(err))

@router.put("/{product_id}", response_model=ProductResponse)
def update(product_id: int, data: ProductUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.isadmin:
        raise HTTPException(status_code=403, detail="Admin access required")
    try:
        return update_product(db, product_id, data)
    except ValueError as err:
        raise HTTPException(status_code=404, detail=str(err))

@router.delete("/{product_id}")
def delete(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.isadmin:
        raise HTTPException(status_code=403, detail="Admin access required")
    try:
        delete_product(db, product_id)
        return {"detail": "Product deactivated successfully"}
    except ValueError as err:
        raise HTTPException(status_code=404, detail=str(err))