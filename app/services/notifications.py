from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from app.core.config import settings
from app.core.redis import set_idempotency_key
from app.worker.celery_app import celery_app


def _to_aware_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC)


async def enqueue_send(payload: dict) -> str:
    # Идемпотентность: если включена и ключ передан, принимаем только первый запрос
    idem_key: str | None = payload.get("idempotency_key")
    if settings.IDEMPOTENCY_ENABLED and idem_key:
        ok = await set_idempotency_key(idem_key)
        if not ok:
            # Возвращаем псевдо task_id, чтобы сохранить стабильный интерфейс
            return f"idem:{idem_key}"

    # В eager-режиме (локально/в тестах) не запускаем задачу внутри запроса.
    # Генерируем task_id и возвращаем его без отправки в Celery.
    if settings.CELERY_TASK_ALWAYS_EAGER:
        return f"eager-{uuid4().hex}"

    eta = None
    schedule_at: datetime | None = payload.get("schedule_at")
    if isinstance(schedule_at, datetime):
        aware = _to_aware_utc(schedule_at)
        now = datetime.now(UTC)
        if aware > now:
            eta = aware

    task = celery_app.send_task("send_notification", args=[payload], eta=eta)
    return task.id
