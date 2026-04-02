from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.stripe_service import handle_webhook_event

router = APIRouter(
    prefix="/webhook",
    tags=["Webhook"]
)

@router.post("/stripe")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    if not sig_header:
        raise HTTPException(status_code=400, detail="Missing stripe-signature header")

    try:
        result = handle_webhook_event(db, payload, sig_header)
        return result
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))