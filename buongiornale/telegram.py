"""Minimal Telegram Bot API client: send a message or a photo to a channel."""

from __future__ import annotations

import requests

_TIMEOUT = 30


def _url(token: str, method: str) -> str:
    return f"https://api.telegram.org/bot{token}/{method}"


def send_message(token: str, chat_id: str, text: str, preview: bool = True) -> None:
    response = requests.post(
        _url(token, "sendMessage"),
        json={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": not preview,
        },
        timeout=_TIMEOUT,
    )
    response.raise_for_status()


def send_photo(token: str, chat_id: str, photo_path: str, caption: str | None = None) -> None:
    with open(photo_path, "rb") as photo:
        response = requests.post(
            _url(token, "sendPhoto"),
            data={"chat_id": chat_id, "caption": caption or "", "parse_mode": "HTML"},
            files={"photo": photo},
            timeout=_TIMEOUT,
        )
    response.raise_for_status()
