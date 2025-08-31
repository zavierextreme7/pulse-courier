from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

# Каталог с шаблонами Jinja2
TEMPLATES_DIR = Path(__file__).resolve().parents[1] / "templates"

_env: Environment | None = None


def get_env() -> Environment:
    global _env
    if _env is None:
        # Создаём каталог при необходимости и инициализируем окружение Jinja2 (асинхронное)
        TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
        _env = Environment(
            loader=FileSystemLoader(str(TEMPLATES_DIR)),
            autoescape=select_autoescape(["html", "xml"]),
            enable_async=True,
        )
    return _env


async def render_template(template_id: str, context: dict) -> str:
    # Асинхронный рендер шаблона с переданным контекстом
    env = get_env()
    tmpl = env.get_template(template_id)
    return await tmpl.render_async(**context)
