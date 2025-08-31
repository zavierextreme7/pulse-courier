from __future__ import annotations

from celery import Celery

from app.core.config import settings

celery_app = Celery("pulse_courier")
celery_app.conf.update(
    broker_url=settings.CELERY_BROKER_URL,
    result_backend=settings.CELERY_RESULT_BACKEND,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# Eager-режим для локальной разработки и тестов, если включён
celery_app.conf.task_always_eager = settings.CELERY_TASK_ALWAYS_EAGER
celery_app.conf.task_eager_propagates = True

# Автоматически находим задачи в этом пакете
celery_app.autodiscover_tasks(["app.worker"], force=True)
