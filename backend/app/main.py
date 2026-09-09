from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth, agents, tasks
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
        "docs": "/api/docs"
    }

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(agents.router, prefix="/api")
app.include_router(tasks.router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 IntelliFlow API starting up...")

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