"""Portfolio endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.core.security import get_current_active_user
from app.db.crud import portfolio as crud_portfolio
from app.db.schemas.portfolio import PortfolioPositionCreate, PortfolioPositionOut, PortfolioSummary
from app.services.portfolio.service import summarise_positions

router = APIRouter()


@router.get("", response_model=list[PortfolioPositionOut])
async def list_positions(user=Depends(get_current_active_user), session: AsyncSession = Depends(get_db)):
    positions = await crud_portfolio.portfolio.list_by_user(session, user.id)
    return positions


@router.post("/positions", response_model=PortfolioPositionOut)
async def create_position(
    payload: PortfolioPositionCreate,
    user=Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db),
):
    data = payload.dict()
    data.update({"user_id": user.id})
    position = await crud_portfolio.portfolio.create(session, data)
    return position


@router.get("/summary", response_model=PortfolioSummary)
async def portfolio_summary(user=Depends(get_current_active_user), session: AsyncSession = Depends(get_db)):
    positions = await crud_portfolio.portfolio.list_by_user(session, user.id)
    summary = summarise_positions(positions)
    return summary
