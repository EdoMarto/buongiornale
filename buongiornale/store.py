"""Remember which articles were already posted, so nothing is sent twice."""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone

from .models import Article


def init_db(path: str) -> None:
    with sqlite3.connect(path) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS seen (key TEXT PRIMARY KEY, posted_at TEXT)")


def unseen(path: str, articles: list[Article]) -> list[Article]:
    init_db(path)
    with sqlite3.connect(path) as conn:
        known = {row[0] for row in conn.execute("SELECT key FROM seen")}
    return [a for a in articles if a.key not in known]


def mark_seen(path: str, articles: list[Article]) -> None:
    init_db(path)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with sqlite3.connect(path) as conn:
        conn.executemany(
            "INSERT OR IGNORE INTO seen (key, posted_at) VALUES (?, ?)",
            [(a.key, now) for a in articles],
        )
