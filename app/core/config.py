from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )

    # Приложение
    APP_NAME: str = "PulseCourier"
    ENV: Literal["local", "dev", "staging", "prod"] = "local"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    PORT: int = Field(default=8000)
    API_PREFIX: str = "/api/v1"

    # Хранилища / Инфраструктура
    DATABASE_URL: str | None = None  # например postgres+asyncpg://user:pass@db:5432/pulse
    REDIS_URL: str = "redis://redis:6379/0"

    # Celery
    CELERY_BROKER_URL: str = "redis://redis:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/2"
    CELERY_TASK_ALWAYS_EAGER: bool = True  # по умолчанию True, чтобы запускать тесты без брокера

    # Провайдеры / вложения
    DEFAULT_PROVIDERS: str = "console"  # перечисление через запятую, в порядке приоритета
    S3_ENDPOINT_URL: AnyUrl | None = None  # для MinIO укажите http://minio:9000
    S3_BUCKET: str | None = None
    AWS_ACCESS_KEY_ID: str | None = None
    AWS_SECRET_ACCESS_KEY: str | None = None
    AWS_REGION: str | None = None

    # Наблюдаемость
    SENTRY_DSN: str | None = None
    OTEL_EXPORTER_OTLP_ENDPOINT: AnyUrl | None = None
    PROMETHEUS_ENABLED: bool = True

    # Флаги возможностей
    RATE_LIMITER_ENABLED: bool = (
        False  # по умолчанию выключен: упрощает локальную разработку и тесты
    )
    IDEMPOTENCY_ENABLED: bool = False

    # Лимиты
    DEFAULT_RATE_LIMIT: str = "20/minute"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]


settings = get_settings()
