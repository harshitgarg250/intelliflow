"""
Main FastAPI Application
यहाँ से सब कुछ start होता है
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app instance बनाएं
app = FastAPI(
    title="IntelliFlow",
    description="🤖 AI Agent Management Platform - Orchestrate intelligent workflows effortlessly",
    version="1.0.0",
    docs_url="/api/docs",        # Swagger UI
    redoc_url="/api/redoc",      # ReDoc
    openapi_url="/api/openapi.json"
)

# CORS Setup
# Frontend अलग port पर है (3000 या 5173), तो CORS चाहिए
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health Check - यह बताता है कि API alive है
@app.get("/api/health")
async def health_check():
    """
    Simple health check endpoint
    Frontend इसे ping करके देखता है कि backend चल रहा है या नहीं
    """
    return {
        "status": "healthy",
        "app_name": "IntelliFlow",
        "version": "1.0.0"
    }

# Root endpoint
@app.get("/")
async def root():
    """
    Root path पर welcome message
    """
    return {
        "message": "Welcome to IntelliFlow",
        "docs": "/api/docs",
        "openapi": "/api/openapi.json"
    }

# App startup event
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 IntelliFlow API starting up...")

# App shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("👋 IntelliFlow API shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
