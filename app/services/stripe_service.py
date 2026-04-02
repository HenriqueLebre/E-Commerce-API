import stripe
from sqlalchemy.orm import Session
from app.core.config import STRIPE_SECRET_KEY
from app.models.order_models import Order, OrderStatus

stripe.api_key = STRIPE_SECRET_KEY

def create_checkout_session(order: Order, base_url: str = "http://localhost:8000") -> str:
    """Creating payment session with Stripe for the given order"""

    line_items = []
    for item in order.items:
        line_items.append({
            "price_data": {
                "currency": "brl",
                "product_data": {
                    "name": f"Product #{item.product_id}",
                },
                "unit_amount": int(item.price * 100),  # Stripe usa centavos
            },
            "quantity": item.quantity,
        })

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url=f"{base_url}/orders/{order.id}?status=success",
        cancel_url=f"{base_url}/orders/{order.id}?status=cancelled",
        metadata={"order_id": str(order.id)}, 
    )

    return session.url

def handle_webhook_event(db: Session, payload: bytes, sig_header: str) -> dict:
    """Event handler for Stripe webhooks, updates order status based on payment events"""
    from app.core.config import STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError:
        raise ValueError("Invalid webhook signature")

    # Pagamento aprovado
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        order_id = int(session["metadata"]["order_id"])

        order = db.query(Order).filter(Order.id == order_id).first()
        if order:
            order.status = OrderStatus.paid
            db.commit()

        return {"status": "paid", "order_id": order_id}

    return {"status": "ignored", "event_type": event["type"]}