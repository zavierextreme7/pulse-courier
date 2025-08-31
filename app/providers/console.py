from __future__ import annotations

from app.core.logging import get_logger
from app.schemas.message import Message

from .base import Provider

logger = get_logger(__name__)


class ConsoleProvider(Provider):
    name = "console"

    async def send(self, msg: Message) -> None:
        logger.info(
            "отправка_в_консоль",
            channel=msg.channel,
            to=msg.to,
            subject=msg.subject,
            template=msg.template_id,
        )
