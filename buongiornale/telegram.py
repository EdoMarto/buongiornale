"""Minimal Telegram Bot API client: send a message or a photo to a channel."""

from __future__ import annotations

import time

import requests

_TIMEOUT = 30
_MAX_RETRIES = 3


def _url(token: str, method: str) -> str:
    return f"https://api.telegram.org/bot{token}/{method}"


def _retry_after(response: requests.Response) -> int | None:
    """Seconds to wait when Telegram answers 429 (too many requests), else None."""
    if response.status_code != 429:
        return None
    try:
        return int(response.json()["parameters"]["retry_after"])
    except (ValueError, KeyError, TypeError):
        pass
    try:
        return int(response.headers.get("Retry-After", 1))
    except (ValueError, TypeError):
        return 1


def send_message(token: str, chat_id: str, text: str, preview: bool = True) -> None:
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": not preview,
    }
    response = None
    for attempt in range(_MAX_RETRIES):
        response = requests.post(_url(token, "sendMessage"), json=payload, timeout=_TIMEOUT)
        wait = _retry_after(response)
        if wait is not None and attempt < _MAX_RETRIES - 1:
            time.sleep(wait)
            continue
        break
    response.raise_for_status()


def send_photo(token: str, chat_id: str, photo_path: str, caption: str | None = None) -> None:
    with open(photo_path, "rb") as photo:
        response = None
        for attempt in range(_MAX_RETRIES):
            photo.seek(0)
            response = requests.post(
                _url(token, "sendPhoto"),
                data={"chat_id": chat_id, "caption": caption or "", "parse_mode": "HTML"},
                files={"photo": photo},
                timeout=_TIMEOUT,
            )
            wait = _retry_after(response)
            if wait is not None and attempt < _MAX_RETRIES - 1:
                time.sleep(wait)
                continue
            break
    response.raise_for_status()
