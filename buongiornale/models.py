"""Core data model: one news article from a feed."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Article:
    title: str
    link: str
    source: str  # outlet name, e.g. "ANSA"
    category: str  # e.g. "Prima pagina", "Economia"
    published: datetime
    summary: str = ""

    @property
    def key(self) -> str:
        """Stable identity for de-duplication and the seen-store."""
        return self.link.split("?")[0].rstrip("/")
