from fastapi import FastAPI
import uvicorn

from src.users.routers import user_router
from src.products.routers import products_router

app = FastAPI()

app.include_router(user_router)
app.include_router(products_router)


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