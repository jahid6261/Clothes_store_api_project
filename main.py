from fastapi import FastAPI,status,Request
import uvicorn
import logging
from src.users.routers import user_router
from src.products.routers import products_router
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.orders.routers import cart_router,order_router
from src.payments.routers import payment_router
from src.admin.routers import admin_router
from src.ai.routers import ai_router
app = FastAPI()

app.include_router(user_router)
app.include_router(products_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(payment_router)
app.include_router(admin_router)
app.include_router(ai_router)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
   
    logger.error(f" Validation Error on path: {request.url.path}")
    logger.error(f" Details: {exc.errors()}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )


@app.get("/")

def read_root():
    return {
        "message":"Welcome to Fastapi Clothe Store Project"
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )