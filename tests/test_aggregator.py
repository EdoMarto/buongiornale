from datetime import datetime, timedelta, timezone

from buongiornale.aggregator import dedupe, group_by_category, recent
from buongiornale.models import Article


def _article(title, link, category="Prima pagina", hours_ago=1):
    return Article(
        title=title,
        link=link,
        source="Test",
        category=category,
        published=datetime.now(timezone.utc) - timedelta(hours=hours_ago),
    )


def test_dedupe_removes_same_link_and_same_title():
    articles = [
        _article("Stessa notizia", "https://x.it/1"),
        _article("Stessa notizia", "https://x.it/1?utm=feed"),  # same link (query stripped)
        _article("Stessa notizia", "https://y.it/2"),  # same title, different link
        _article("Altra notizia", "https://z.it/3"),
    ]
    assert len(dedupe(articles)) == 2


def test_recent_filters_old_articles():
    articles = [_article("Fresca", "https://x.it/1", hours_ago=2), _article("Vecchia", "https://x.it/2", hours_ago=48)]
    titles = [a.title for a in recent(articles, hours=24)]
    assert titles == ["Fresca"]


def test_group_caps_per_category():
    articles = [_article(f"N{i}", f"https://x.it/{i}") for i in range(10)]
    grouped = group_by_category(articles, max_per_category=3)
    assert len(grouped["Prima pagina"]) == 3
