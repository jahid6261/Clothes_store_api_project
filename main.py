from fastapi import FastAPI,status,Request,APIRouter
import uvicorn
import logging

from src.users.routers import user_router
from src.products.routers import products_router,category_router
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.orders.routers import cart_router,order_router
from src.payments.routers import payment_router
from src.admin.routers import admin_router
from src.ai.routers import ai_router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

api_v1=APIRouter(prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


api_v1.include_router(user_router)
api_v1.include_router(category_router)
api_v1.include_router(products_router)
api_v1.include_router(cart_router)
api_v1.include_router(order_router)
api_v1.include_router(payment_router)
api_v1.include_router(admin_router)

api_v1.include_router(ai_router)

app.include_router(api_v1)



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