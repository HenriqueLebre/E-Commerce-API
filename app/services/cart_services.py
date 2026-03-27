from sqlalchemy.orm import Session
from app.models.cart import Cart, CartItem
from app.models.product import Product
from app.schemas.cart import CartItemCreate, CartItemUpdate

def get_or_create_cart(db: Session, user_id: int) -> Cart:
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart

def add_item(db: Session, user_id: int, data: CartItemCreate) -> Cart:
    product = db.query(Product).filter(Product.id == data.product_id, Product.active == True).first()
    if not product:
        raise ValueError("Product not found")
    if data.quantity > product.stock:
        raise ValueError(f"Insufficient stock. Available: {product.stock}")

    cart = get_or_create_cart(db, user_id)

    # Se o produto já está no carrinho, incrementa
    existing_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == data.product_id
    ).first()

    if existing_item:
        existing_item.quantity += data.quantity
        if existing_item.quantity > product.stock:
            raise ValueError(f"Insufficient stock. Available: {product.stock}")
    else:
        new_item = CartItem(
            cart_id=cart.id,
            product_id=data.product_id,
            quantity=data.quantity
        )
        db.add(new_item)

    db.commit()
    db.refresh(cart)
    return format_cart(db, cart)

def get_cart(db: Session, user_id: int) -> dict:
    cart = get_or_create_cart(db, user_id)
    return format_cart(db, cart)

def update_item(db: Session, user_id: int, item_id: int, data: CartItemUpdate) -> dict:
    cart = get_or_create_cart(db, user_id)
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart.id).first()
    if not item:
        raise ValueError("Item not found in cart")

    product = db.query(Product).filter(Product.id == item.product_id).first()
    if data.quantity > product.stock:
        raise ValueError(f"Insufficient stock. Available: {product.stock}")

    item.quantity = data.quantity
    db.commit()
    db.refresh(cart)
    return format_cart(db, cart)

def remove_item(db: Session, user_id: int, item_id: int) -> dict:
    cart = get_or_create_cart(db, user_id)
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart.id).first()
    if not item:
        raise ValueError("Item not found in cart")

    db.delete(item)
    db.commit()
    db.refresh(cart)
    return format_cart(db, cart)

def clear_cart(db: Session, user_id: int) -> dict:
    cart = get_or_create_cart(db, user_id)
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    db.commit()
    db.refresh(cart)
    return format_cart(db, cart)

def format_cart(db: Session, cart: Cart) -> dict:
    items = []
    total = 0
    for item in cart.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        items.append({
            "id": item.id,
            "product_id": item.product_id,
            "quantity": item.quantity,
            "product_name": product.name if product else None,
            "product_price": float(product.price) if product else None
        })
        if product:
            total += float(product.price) * item.quantity

    return {
        "id": cart.id,
        "items": items,
        "total": round(total, 2)
    }