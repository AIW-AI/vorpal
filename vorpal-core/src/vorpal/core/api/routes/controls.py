"""Controls API endpoints."""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from vorpal.core.api.schemas.common import PaginationMeta
from vorpal.core.api.schemas.control import (
    ControlCreate,
    ControlListResponse,
    ControlResponse,
    ControlUpdate,
)
from vorpal.core.db import get_session
from vorpal.core.models.control import Control, ControlCategory

router = APIRouter()


@router.get("", response_model=ControlListResponse)
async def list_controls(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=100),
    category: ControlCategory | None = None,
    regulation: str | None = None,
    db: AsyncSession = Depends(get_session),
) -> dict[str, Any]:
    """List governance controls with optional filtering."""
    query = select(Control)

    # Apply filters
    if category:
        query = query.where(Control.category == category)
    if regulation:
        query = query.where(Control.regulation == regulation)

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query) or 0

    # Apply pagination
    query = query.offset((page - 1) * page_size).limit(page_size)
    query = query.order_by(Control.id)

    result = await db.execute(query)
    controls = result.scalars().all()

    return {
        "data": [ControlResponse.model_validate(c) for c in controls],
        "meta": PaginationMeta(
            page=page,
            page_size=page_size,
            total=total,
            total_pages=(total + page_size - 1) // page_size,
        ),
    }


@router.post("", response_model=ControlResponse, status_code=status.HTTP_201_CREATED)
async def create_control(
    control_in: ControlCreate,
    db: AsyncSession = Depends(get_session),
) -> Control:
    """Create a new governance control."""
    # Check if control ID already exists
    existing = await db.execute(select(Control).where(Control.id == control_in.id))
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Control {control_in.id} already exists",
        )

    control = Control(
        id=control_in.id,
        name=control_in.name,
        description=control_in.description,
        category=control_in.category,
        regulation=control_in.regulation,
        requirement_text=control_in.requirement_text,
        test_guidance=control_in.test_guidance,
        mandatory=control_in.mandatory,
        applies_to_risk_tiers=control_in.applies_to_risk_tiers,
    )

    db.add(control)
    await db.flush()
    await db.refresh(control)

    return control


@router.get("/{control_id}", response_model=ControlResponse)
async def get_control(
    control_id: str,
    db: AsyncSession = Depends(get_session),
) -> Control:
    """Get a specific control by ID."""
    result = await db.execute(select(Control).where(Control.id == control_id))
    control = result.scalar_one_or_none()

    if not control:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Control {control_id} not found",
        )

    return control


@router.patch("/{control_id}", response_model=ControlResponse)
async def update_control(
    control_id: str,
    control_in: ControlUpdate,
    db: AsyncSession = Depends(get_session),
) -> Control:
    """Update a governance control."""
    result = await db.execute(select(Control).where(Control.id == control_id))
    control = result.scalar_one_or_none()

    if not control:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Control {control_id} not found",
        )

    # Update only provided fields
    update_data = control_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(control, field, value)

    await db.flush()
    await db.refresh(control)

    return control


@router.delete("/{control_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_control(
    control_id: str,
    db: AsyncSession = Depends(get_session),
) -> None:
    """Delete a governance control."""
    result = await db.execute(select(Control).where(Control.id == control_id))
    control = result.scalar_one_or_none()

    if not control:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Control {control_id} not found",
        )

    await db.delete(control)
    await db.flush()
