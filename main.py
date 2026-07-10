from fastapi import FastAPI
import uvicorn

app = FastAPI()


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