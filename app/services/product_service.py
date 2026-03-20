from re import search
from unicodedata import category

from sqlalchemy.orm import Session
from datetime import datetime
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

def create_product(db: Session, product: ProductCreate) -> Product:
    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        category=product.category,
        image_url=product.image_url
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product;

def get_products(db: Session,
                search: str = None,
                category: str = None,
                min_price: float = None,
                max_price: float = None,
                page: int = 1,
                size: int = 20,
                sort_by: str = "datecreation",
                order: str = "desc") -> dict:
    query = db.query(Product).filter(Product.active == True)

    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    if category:
        query = query.filter(Product.category == category)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    
    total =  query.count()
    
    sort_column = getattr(Product, sort_by, Product.datecreation)
    if order == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())
    
    skip = (page - 1 ) * size
    items = query.offset(skip).limit(size).all()
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "size": size,
        "pages": (total + size - 1) // size
    }

def get_product_by_id(db: Session, product_id: int) -> Product:
    product = db.query(Product).filter(Product.id == product_id, Product.active == True).first()
    if not product:
        raise ValueError("Product not found")
    return product;

def update_product(db: Session, product_id: int, data: ProductUpdate) -> Product:
    product = get_product_by_id(db, product_id)
    
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)
    
    db.commit()
    db.refresh(product)
    return product;

def delete_product(db: Session, product_id: int) -> Product:
    product = get_product_by_id(db, product_id)
    product.active = False
    product.datedeactivated = datetime.utcnow()
    db.commit()
    db.refresh(product)
    return product;