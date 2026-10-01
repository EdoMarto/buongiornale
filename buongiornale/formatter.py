"""Build the Telegram messages (HTML), split to stay under Telegram's size limit."""

from __future__ import annotations

import html
from datetime import datetime

from .models import Article

_MAX = 3800  # Telegram's hard limit is 4096; leave headroom.

_GIORNI = ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"]
_MESI = [
    "gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno",
    "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre",
]
_CATEGORY_ICON = {"Prima pagina": "🏛", "Economia": "💶", "Tecnologia": "💻", "Sport": "⚽"}


def italian_date(dt: datetime) -> str:
    return f"{_GIORNI[dt.weekday()]} {dt.day} {_MESI[dt.month - 1]} {dt.year}"


def _headline(article: Article) -> str:
    return f'• <a href="{html.escape(article.link)}">{html.escape(article.title)}</a> — <i>{html.escape(article.source)}</i>'


def digest_messages(grouped: dict[str, list[Article]], now: datetime) -> list[str]:
    """One or more messages: a header, then a section per category."""
    header = f"🗞 <b>Buongiornale</b> — {italian_date(now)}\nLe notizie del giorno dalle principali testate.\n"

    messages: list[str] = []
    current = header
    for category, articles in grouped.items():
        if not articles:
            continue
        section = f"\n<b>{_CATEGORY_ICON.get(category, '📰')} {html.escape(category)}</b>\n"
        section += "\n".join(_headline(a) for a in articles) + "\n"

        if len(current) + len(section) > _MAX:
            messages.append(current.rstrip())
            current = section.lstrip("\n")
        else:
            current += section

    if current.strip():
        messages.append(current.rstrip())
    return messages


def article_message(article: Article) -> str:
    """A single-article post for the live stream mode."""
    icon = _CATEGORY_ICON.get(article.category, "📰")
    return (
        f"{icon} <b>{html.escape(article.title)}</b>\n"
        f"<i>{html.escape(article.source)} · {html.escape(article.category)}</i>\n"
        f'<a href="{html.escape(article.link)}">Leggi l\'articolo</a>'
    )
