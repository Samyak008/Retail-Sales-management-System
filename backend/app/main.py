import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import sales

app = FastAPI(title="Retail Sales Management API", version="0.1.0")

# Get allowed origins from environment or use defaults
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://.*\.vercel\.app",  # Allow all Vercel deployments
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sales.router, prefix="/api")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
