from __future__ import annotations

from celery import shared_task

from app.core.config import settings
from app.core.logging import get_logger
from app.core.templates import render_template
from app.providers.base import load_providers
from app.schemas.message import Message

logger = get_logger(__name__)


@shared_task(name="send_notification")
def send_notification_task(payload: dict) -> dict:
    # Задачи Celery лучше держать синхронными — проще сериализация и запуск
    import asyncio

    async def _run():
        msg = Message.model_validate(payload)
        providers = load_providers(
            msg.provider_preferences or settings.DEFAULT_PROVIDERS.split(",")
        )

        # Рендерим шаблон, если он указан
        if msg.template_id:
            if not msg.body_html:
                msg.body_html = await render_template(msg.template_id, msg.template_vars)

        last_error: Exception | None = None
        for p in providers:
            try:
                await p.send(msg)
                logger.info("отправка_успех", provider=p.name)
                return {"status": "sent", "provider": p.name}
            except Exception as e:  # noqa: BLE001
                logger.warning("отправка_ошибка_провайдер", provider=p.name, error=str(e))
                last_error = e
        if last_error:
            raise last_error
        return {"status": "sent"}

    return asyncio.run(_run())
