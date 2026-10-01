from datetime import datetime, timezone

from buongiornale.formatter import article_message, digest_messages, italian_date
from buongiornale.models import Article


def _article(title, category="Prima pagina"):
    return Article(title, "https://x.it/a", "ANSA", category, datetime.now(timezone.utc))


def test_italian_date():
    assert italian_date(datetime(2026, 10, 1)) == "giovedì 1 ottobre 2026"


def test_digest_has_header_and_escapes_html():
    grouped = {"Prima pagina": [_article("Borsa & spread <giù>")]}
    messages = digest_messages(grouped, datetime(2026, 10, 1))
    assert messages and "Buongiornale" in messages[0]
    assert "&amp;" in messages[0] and "&lt;giù&gt;" in messages[0]


def test_article_message_contains_link_and_source():
    msg = article_message(_article("Titolo", "Tecnologia"))
    assert "Titolo" in msg and "ANSA" in msg and "https://x.it/a" in msg
