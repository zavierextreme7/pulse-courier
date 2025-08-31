from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field, HttpUrl


class Channel(str, Enum):
    email = "email"
    sms = "sms"
    push = "push"
    slack = "slack"
    telegram = "telegram"


class Attachment(BaseModel):
    filename: str
    content_type: str
    url: HttpUrl | None = None
    s3_key: str | None = None


class Message(BaseModel):
    channel: Channel
    to: list[str] = Field(default_factory=list)
    subject: str | None = None
    body_text: str | None = None
    body_html: str | None = None

    template_id: str | None = None
    template_vars: dict[str, Any] = Field(default_factory=dict)

    attachments: list[Attachment] = Field(default_factory=list)

    idempotency_key: str | None = None
    provider_preferences: list[str] = Field(default_factory=list)
    schedule_at: datetime | None = None

    metadata: dict[str, Any] = Field(default_factory=dict)


class EnqueueResult(BaseModel):
    task_id: str
    status: Literal["queued"] = "queued"
