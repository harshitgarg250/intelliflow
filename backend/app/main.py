"""
Main FastAPI Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth
from app.database import init_db, close_db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="IntelliFlow",
    description="🤖 AI Agent Management Platform - Orchestrate intelligent workflows effortlessly",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# CORS Middleware
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


# Health Check
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "app_name": "IntelliFlow",
        "version": "1.0.0"
    }


@app.get("/")
async def root():
    return {
        "message": "Welcome to IntelliFlow",
        "docs": "/api/docs",
        "openapi": "/api/openapi.json"
    }


# Include routers
app.include_router(auth.router, prefix="/api", tags=["Authentication"])


# Startup
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 IntelliFlow API starting up...")

    try:
        await init_db()
        logger.info("✅ Database initialized successfully")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise


# Shutdown
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("👋 IntelliFlow API shutting down...")

    try:
        await close_db()
    except Exception as e:
        logger.error(f"❌ Database shutdown error: {e}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )