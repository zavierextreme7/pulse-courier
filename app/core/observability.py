from __future__ import annotations

import sentry_sdk
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from .config import settings
from .logging import get_logger

logger = get_logger(__name__)


def init_sentry() -> None:
    if settings.SENTRY_DSN:
        sentry_sdk.init(dsn=settings.SENTRY_DSN, traces_sample_rate=0.1)
        # Инициализация Sentry завершена
        logger.info("sentry_инициализирован")


def init_otel(app=None) -> None:
    if not settings.OTEL_EXPORTER_OTLP_ENDPOINT:
        return
    # Ресурсы и провайдер трассировок
    resource = Resource(
        attributes={"service.name": settings.APP_NAME, "deployment.environment": settings.ENV}
    )
    provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(
        OTLPSpanExporter(endpoint=str(settings.OTEL_EXPORTER_OTLP_ENDPOINT))
    )
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)
    if app is not None:
        FastAPIInstrumentor.instrument_app(app)
    logger.info("otel_инициализирован", endpoint=settings.OTEL_EXPORTER_OTLP_ENDPOINT)
