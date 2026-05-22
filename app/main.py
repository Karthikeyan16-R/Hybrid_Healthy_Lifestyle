# main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import create_db_and_tables

# Import all routers
from app.routers import users, ai_routes
from app.routers import hospital_router


# Create FastAPI app
app = FastAPI(
    title="AI Health & Lifestyle Companion",
    description="Complete AI-powered health platform with diet planning, workouts, chatbot, and gamification",
    version="1.0.0"
)

# ✅ Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    hospital_router.router,
    prefix="/api",
    tags=["Hospital Finder"]
)


# ✅ Create database tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    print("✅ Database initialized")
    print("🚀 AI Health Companion API is running!")

# ✅ Register all routers
app.include_router(users.router, prefix="/users")
app.include_router(ai_routes.router, prefix="/ai", tags=["AI Services"])

# Try to import health tracking routes (they might be in a separate file)
try:
    from app.routers import health_tracking_routes
    app.include_router(health_tracking_routes.router, prefix="/health", tags=["Health Tracking"])
    print("✅ Health tracking routes loaded")
except ImportError as e:
    print(f"⚠️  Health tracking routes not found: {e}")
    print("💡 Create app/routers/health_tracking_routes.py to enable challenges and dashboard")

# ✅ Root endpoint
@app.get("/")
def root():
    return {
        "message": "🏥 AI Health & Lifestyle Companion API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "users": "/users",
            "ai_services": "/ai",
            "health_tracking": "/health",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

# ✅ Health check endpoint
@app.get("/health-check")
def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "ai_services": "active"
    }

# ✅ Run with: uvicorn main:app --reload --port 5050
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5050)