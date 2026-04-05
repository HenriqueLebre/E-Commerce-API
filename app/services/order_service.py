from sqlalchemy.orm import Session
from app.models.cart_models import Cart, CartItem
from app.models.order_models import Order, OrderItem, OrderStatus
from app.models.product_models import Product
from app.core.exceptions import NotFoundException, BadRequestException
from app.services.stripe_service import create_checkout_session

def create_order(db: Session, user_id: int) -> dict:
    try:
        cart = db.query(Cart).filter(Cart.user_id == user_id).first()
        if not cart or not cart.items:
            raise BadRequestException("Cart is empty")

        total = 0
        for item in cart.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if not product or not product.active:
                raise NotFoundException(f"Product {item.product_id} not available")
            if item.quantity > product.stock:
                raise BadRequestException(f"Insufficient stock for {product.name}. Available: {product.stock}")
            total += float(product.price) * item.quantity

        order = Order(
            user_id=user_id,
            status=OrderStatus.pending,
            total=round(total, 2)
        )
        db.add(order)
        db.flush()

        for item in cart.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=float(product.price)
            )
            db.add(order_item)
            product.stock -= item.quantity

        db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()

        db.commit()
        db.refresh(order)

        payment_url = create_checkout_session(order)
        return {"order": order, "payment_url": payment_url}

    except (NotFoundException, BadRequestException):
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise