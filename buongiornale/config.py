"""Configuration, read from environment variables (and a local .env file)."""

from __future__ import annotations

import os
from dataclasses import dataclass

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # python-dotenv is optional
    pass


def _int_env(name: str, default: str) -> int:
    raw = os.environ.get(name, default)
    try:
        return int(raw)
    except (ValueError, TypeError):
        raise ValueError(f"{name} must be an integer, got {raw!r}") from None


@dataclass
class Config:
    telegram_token: str | None
    channel: str | None  # e.g. "@BuonGiornale" or a numeric chat id
    feeds_file: str
    digest_hours: int  # how far back the morning digest looks
    max_per_category: int  # headlines per category in the digest
    db_path: str
    logo_path: str

    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            telegram_token=os.environ.get("TELEGRAM_BOT_TOKEN"),
            channel=os.environ.get("TELEGRAM_CHANNEL"),
            feeds_file=os.environ.get("FEEDS_FILE", "feeds.json"),
            digest_hours=_int_env("DIGEST_HOURS", "24"),
            max_per_category=_int_env("MAX_PER_CATEGORY", "6"),
            db_path=os.environ.get("DB_PATH", "buongiornale.db"),
            logo_path=os.environ.get("LOGO_PATH", "docs/logo.png"),
        )
