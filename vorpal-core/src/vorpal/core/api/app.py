"""FastAPI application factory."""

from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from vorpal.core.config import get_settings
from vorpal.core.db import close_db, init_db


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    """Application lifespan handler."""
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title="Vorpal Core",
        description="AI Governance Registry, Policy Engine, and Audit Trail",
        version=settings.app_version,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    from vorpal.core.api.routes import health, systems, controls, policies, audit

    app.include_router(health.router, tags=["Health"])
    app.include_router(systems.router, prefix="/api/v1/systems", tags=["Systems"])
    app.include_router(controls.router, prefix="/api/v1/controls", tags=["Controls"])
    app.include_router(policies.router, prefix="/api/v1/policies", tags=["Policies"])
    app.include_router(audit.router, prefix="/api/v1/audit", tags=["Audit"])

    return app


# Default app instance
app = create_app()


@app.get("/")
async def root() -> dict[str, Any]:
    """Root endpoint with API information."""
    settings = get_settings()
    return {
        "name": "Vorpal Core",
        "version": settings.app_version,
        "docs": "/docs",
        "openapi": "/openapi.json",
    }
