# app/main.py
from fastapi import FastAPI
from app.routers.auth_user import router as auth_router
from app.routers import product_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(product_router.router)

@app.get("/health")
def health():
    return {"status": "ok"}

