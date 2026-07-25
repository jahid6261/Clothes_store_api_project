from fastapi import FastAPI,status,Request
import uvicorn
import logging
from src.users.routers import user_router
from src.products.routers import products_router
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
app = FastAPI()

app.include_router(user_router)
app.include_router(products_router)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Validation error হলে টার্মিনালে ফুল এরর প্রিন্ট করার হ্যান্ডলার
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # ডকার বা টার্মিনাল লগে বিস্তারিত দেখাবে
    logger.error(f"❌ Validation Error on path: {request.url.path}")
    logger.error(f"❌ Details: {exc.errors()}")

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