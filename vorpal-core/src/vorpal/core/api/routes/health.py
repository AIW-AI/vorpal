"""Health check endpoints."""

from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from vorpal.core.config import get_settings
from vorpal.core.db import get_session

router = APIRouter()


@router.get("/health")
async def health_check() -> dict[str, str]:
    """Basic health check."""
    return {"status": "healthy"}


@router.get("/ready")
async def readiness_check(
    db: AsyncSession = Depends(get_session),
) -> dict[str, Any]:
    """Readiness check including database connectivity."""
    settings = get_settings()

    # Check database connection
    try:
        await db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {e}"

    return {
        "status": "ready" if db_status == "connected" else "degraded",
        "version": settings.app_version,
        "checks": {
            "database": db_status,
        },
    }
