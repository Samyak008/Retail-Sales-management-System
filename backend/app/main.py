from fastapi import FastAPI

from .routers import sales

app = FastAPI(title="Retail Sales Management API", version="0.1.0")

app.include_router(sales.router, prefix="/api")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
