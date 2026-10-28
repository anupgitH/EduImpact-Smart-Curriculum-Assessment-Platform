
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.session import Base, engine
from app import models
from app.api.routes import auth, courses, assessments, ai, analytics


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database tables for non-production environments."""
    if settings.auto_create_tables and settings.environment != "production":
        Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="EduImpact curriculum and assessment API",
    debug=settings.debug,
    lifespan=lifespan,
)

# Local development origins for React/Vite.
allowed_origins = list(
    set(
        settings.cors_origin_list
        + [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:5174",
            "http://127.0.0.1:5174",
            "http://localhost:4173",
            "http://127.0.0.1:4173",
        ]
    )
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["health"])
def root():
    return {
        "message": "Welcome to EduImpact API",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health", tags=["health"])
def health():
    return {
        "status": "ok",
        "service": "eduimpact-api",
        "environment": settings.environment,
    }


app.include_router(auth.router, prefix="/api/v1")
app.include_router(courses.router, prefix="/api/v1")
app.include_router(assessments.router, prefix="/api/v1")
app.include_router(ai.router, prefix="/api/v1")
app.include_router(analytics.router, prefix="/api/v1")
