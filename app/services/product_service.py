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

def get_products(db: Session) -> list[Product]:
    return db.query(Product).filter(Product.active == True).all();

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