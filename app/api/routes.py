from __future__ import annotations

from collections.abc import Callable
from typing import Any

from fastapi import APIRouter, Depends

from app.core.config import settings
from app.schemas.message import EnqueueResult, Message
from app.services.notifications import enqueue_send

router = APIRouter()

# Условная зависимость для ограничителя скорости
rl_dep: Callable[..., Any] | None = None
if settings.RATE_LIMITER_ENABLED:
    try:
        from fastapi_limiter.depends import RateLimiter

        # Простое значение по умолчанию: 20 запросов за 60 секунд
        rl_dep = RateLimiter(times=20, seconds=60)
    except ImportError:  # pragma: no cover - if not installed
        rl_dep = None


@router.get("/health")
async def health() -> dict:
    return {"status": "ok", "app": settings.APP_NAME, "env": settings.ENV}


@router.post(
    "/notifications/send",
    response_model=EnqueueResult,
    dependencies=([Depends(rl_dep)] if rl_dep else None),
)
async def send(msg: Message) -> EnqueueResult:
    task_id = await enqueue_send(msg.model_dump())
    return EnqueueResult(task_id=task_id)
