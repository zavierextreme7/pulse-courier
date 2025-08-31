from __future__ import annotations

from abc import ABC, abstractmethod

from app.schemas.message import Message


class Provider(ABC):
    name: str

    @abstractmethod
    async def send(self, msg: Message) -> None:  # Должен бросать исключение при ошибке
        raise NotImplementedError


def load_providers(names: list[str]) -> list[Provider]:
    # Простой динамический реестр; позже дополним реальными провайдерами
    providers: list[Provider] = []
    for n in names:
        n = n.strip().lower()
        if n == "console":
            from .console import ConsoleProvider

            providers.append(ConsoleProvider())
        # Будущее: ses, sendgrid, twilio, fcm, slack, telegram
    if not providers:
        from .console import ConsoleProvider

        providers.append(ConsoleProvider())
    return providers
