from app.core.exceptions import (
    NotFoundException, BadRequestException,
    ForbiddenException, ConflictException
)
from app.core.error_handlers import (
    not_found_handler, bad_request_handler,
    forbidden_handler, conflict_handler, generic_handler
)
from app.routers import auth_router, product_router, cart_router, order_router, user_router, webhook_router

app = FastAPI(title="E-Commerce API")

app.add_exception_handler(NotFoundException, not_found_handler)
app.add_exception_handler(BadRequestException, bad_request_handler)
app.add_exception_handler(ForbiddenException, forbidden_handler)
app.add_exception_handler(ConflictException, conflict_handler)
app.add_exception_handler(Exception, generic_handler)

app.include_router(auth_router.router)
app.include_router(product_router.router)
app.include_router(cart_router.router)
app.include_router(order_router.router)
app.include_router(webhook_router.router)
app.include_router(user_router.router)

@app.get("/health")
def health():
    return {"status": "ok"}

