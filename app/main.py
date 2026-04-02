# app/main.py
from fastapi import FastAPI
from app.routers.auth_user import router as auth_router
from app.routers import product_router
from app.routers import cart_router
from app.routers import order_router
from app.routers import webhook_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(product_router.router)
app.include_router(cart_router.router)
app.include_router(order_router.router)
app.include_router(webhook_router.router)

@app.get("/health")
def health():
    return {"status": "ok"}

