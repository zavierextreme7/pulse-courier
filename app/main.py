from __future__ import annotations

import uvicorn
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.routes import router as api_router
from app.core.config import settings
from app.core.logging import configure_logging
from app.core.observability import init_otel, init_sentry
from app.core.redis import get_redis


def create_app() -> FastAPI:
    configure_logging(level=settings.LOG_LEVEL, json=(settings.ENV in {"staging", "prod"}))

    app = FastAPI(title=settings.APP_NAME)

    # Наблюдаемость
    init_sentry()
    init_otel(app)

    # Метрики
    if settings.PROMETHEUS_ENABLED:
        Instrumentator().instrument(app).expose(app, include_in_schema=False)

    # На старте: инициализируем ограничитель скорости, если включён
    if settings.RATE_LIMITER_ENABLED:

        @app.on_event("startup")
        async def _init_rate_limiter() -> None:  # noqa: D401
            """Инициализируем ограничитель скорости (rate limiter)."""
            redis = await get_redis()
            await FastAPILimiter.init(redis)

    # Маршруты
    app.include_router(api_router, prefix=settings.API_PREFIX)
    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.PORT, reload=True)
