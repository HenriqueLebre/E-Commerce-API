# app/services/order_service.py

from sqlalchemy.orm import Session
from app.models.cart_models import Cart, CartItem
from app.models.order_models import Order, OrderItem, OrderStatus
from app.models.product_models import Product
from app.services.stripe_service import create_checkout_session

def create_order(db: Session, user_id: int) -> dict:
    try:
        # 1. Buscar carrinho
        cart = db.query(Cart).filter(Cart.user_id == user_id).first()
        if not cart or not cart.items:
            raise ValueError("Cart is empty")

        # 2. Validar estoque e calcular total
        total = 0
        for item in cart.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if not product or not product.active:
                raise ValueError(f"Product {item.product_id} not available")
            if item.quantity > product.stock:
                raise ValueError(f"Insufficient stock for {product.name}. Available: {product.stock}")
            total += float(product.price) * item.quantity

        # 3. Criar pedido
        order = Order(
            user_id=user_id,
            status=OrderStatus.pending,
            total=round(total, 2)
        )
        db.add(order)
        db.flush()  # gera o order.id sem commitar

        # 4. Criar itens do pedido + decrementar estoque
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

        # 5. Limpar carrinho
        db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()

        db.commit()
        db.refresh(order)

                # Gera link de pagamento
        payment_url = create_checkout_session(order)

        return {
                    "order": order,
                    "payment_url": payment_url
                }

    except Exception:
        db.rollback()
        raise;




def get_orders(db: Session, user_id: int) -> list[Order]:
    return db.query(Order).filter(Order.user_id == user_id).all()

def get_order_by_id(db: Session, user_id: int, order_id: int) -> Order:
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()
    if not order:
        raise ValueError("Order not found")
    return order