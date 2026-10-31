"""Fetch the configured RSS feeds and turn them into a clean list of articles."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta, timezone

import feedparser

from .models import Article

log = logging.getLogger(__name__)


def load_feeds(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def _published(entry) -> datetime:
    parsed = entry.get("published_parsed") or entry.get("updated_parsed")
    if parsed:
        return datetime(*parsed[:6], tzinfo=timezone.utc)
    return datetime.now(timezone.utc)


def fetch(feeds: list[dict]) -> list[Article]:
    """Download every feed and flatten it into Article objects."""
    articles: list[Article] = []
    for feed in feeds:
        try:
            url = (feed.get("url") or "").strip()
            source = (feed.get("source") or "?").strip()
            category = (feed.get("category") or "").strip()
            if not url or not category:
                log.warning("Skipping feed with missing url/category: %r", feed)
                continue
            parsed = feedparser.parse(url)
            if getattr(parsed, "status", 200) >= 400 or not parsed.entries:
                log.warning("Feed %s returned no entries (status %s)", source, getattr(parsed, "status", "?"))
                continue
            for entry in parsed.entries:
                title = (entry.get("title") or "").strip()
                link = (entry.get("link") or "").strip()
                if not title or not link:
                    continue
                articles.append(
                    Article(
                        title=title,
                        link=link,
                        source=source,
                        category=category,
                        published=_published(entry),
                    )
                )
        except Exception:
            # One bad feed or malformed entry should not abort the whole run.
            log.exception("Failed to process feed %r", feed)
            continue
    log.info("Fetched %d articles from %d feeds", len(articles), len(feeds))
    return articles


def dedupe(articles: list[Article]) -> list[Article]:
    """Drop repeats by link and by identical title, keeping the newest."""
    seen_keys: set[str] = set()
    seen_titles: set[str] = set()
    out: list[Article] = []
    for article in sorted(articles, key=lambda a: a.published, reverse=True):
        title = article.title.lower()
        if article.key in seen_keys or title in seen_titles:
            continue
        seen_keys.add(article.key)
        seen_titles.add(title)
        out.append(article)
    return out


def recent(articles: list[Article], hours: int) -> list[Article]:
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    return [a for a in articles if a.published >= cutoff]


def group_by_category(articles: list[Article], max_per_category: int) -> dict[str, list[Article]]:
    grouped: dict[str, list[Article]] = {}
    for article in articles:
        bucket = grouped.setdefault(article.category, [])
        if len(bucket) < max_per_category:
            bucket.append(article)
    return grouped
