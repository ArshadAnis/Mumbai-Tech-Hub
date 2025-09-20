"""News and calendar endpoints."""
from __future__ import annotations

from fastapi import APIRouter

from app.services.news.service import fetch_news
from app.services.calendar.service import fetch_calendar

router = APIRouter()


@router.get("/news")
async def news():
    return await fetch_news()


@router.get("/calendar")
async def calendar():
    return await fetch_calendar()
