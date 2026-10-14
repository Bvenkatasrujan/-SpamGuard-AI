"""
FastAPI Main Application Entry Point for SpamGuard AI REST Service.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api import health, prediction, model

app = FastAPI(
    title="SpamGuard AI REST API",
    description="Production-grade REST API for SpamGuard AI Reusable Hybrid NLP Spam Detection Engine.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS Middleware for Frontend & External Client Access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins during local dev & demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API v1 Routers
app.include_router(health.router, prefix="/api/v1")
app.include_router(prediction.router, prefix="/api/v1")
app.include_router(model.router, prefix="/api/v1")

@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": "Welcome to SpamGuard AI REST API",
        "documentation": "/docs",
        "health": "/api/v1/health"
    }
