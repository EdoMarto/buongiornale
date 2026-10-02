"""Entry point. Two modes:

    digest  - a morning roundup grouped by category (run once a day)
    stream  - post every new article since the last run (run often)
"""

from __future__ import annotations

import argparse
import logging
import sys
from datetime import datetime

from . import aggregator, store
from .config import Config
from .formatter import article_message, digest_messages
from .telegram import send_message, send_photo

log = logging.getLogger("buongiornale")


def _print_preview(messages: list[str]) -> None:
    for i, message in enumerate(messages, 1):
        print(f"\n----- message {i}/{len(messages)} -----\n{message}")


def run_digest(config: Config, send: bool, with_logo: bool) -> int:
    feeds = aggregator.load_feeds(config.feeds_file)
    articles = aggregator.dedupe(aggregator.fetch(feeds))
    articles = aggregator.recent(articles, config.digest_hours)
    grouped = aggregator.group_by_category(articles, config.max_per_category)
    messages = digest_messages(grouped, datetime.now())

    if not any(grouped.values()):
        log.info("Nothing to publish in the last %d h", config.digest_hours)
        return 0

    if not send:
        _print_preview(messages)
        return len(messages)

    if with_logo:
        send_photo(config.telegram_token, config.channel, config.logo_path, caption=messages[0])
        messages = messages[1:]
    for message in messages:
        send_message(config.telegram_token, config.channel, message, preview=False)
    log.info("Posted digest (%d message(s)) to %s", len(messages) + (1 if with_logo else 0), config.channel)
    return 1


def run_stream(config: Config, send: bool) -> int:
    feeds = aggregator.load_feeds(config.feeds_file)
    articles = aggregator.dedupe(aggregator.fetch(feeds))
    articles = aggregator.recent(articles, config.digest_hours)
    fresh = store.unseen(config.db_path, articles)
    fresh.sort(key=lambda a: a.published)  # oldest first, so the channel reads top-to-bottom
    log.info("%d new article(s)", len(fresh))

    if not send:
        _print_preview([article_message(a) for a in fresh])
        return len(fresh)

    for article in fresh:
        send_message(config.telegram_token, config.channel, article_message(article))
    store.mark_seen(config.db_path, fresh)
    return len(fresh)


def main(argv: list[str] | None = None) -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    for stream_io in (sys.stdout, sys.stderr):  # emoji-safe console on Windows
        try:
            stream_io.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass

    parser = argparse.ArgumentParser(description="Publish the day's news to a Telegram channel.")
    parser.add_argument("mode", choices=["digest", "stream"], help="morning roundup, or live stream of new items")
    parser.add_argument("--dry-run", action="store_true", help="print the messages instead of posting")
    parser.add_argument("--no-logo", action="store_true", help="digest: do not post the logo image first")
    args = parser.parse_args(argv)

    config = Config.from_env()
    send = not args.dry_run
    if send and not (config.telegram_token and config.channel):
        log.warning("TELEGRAM_BOT_TOKEN / TELEGRAM_CHANNEL not set, switching to dry run.")
        send = False

    if args.mode == "digest":
        run_digest(config, send, with_logo=not args.no_logo)
    else:
        run_stream(config, send)


if __name__ == "__main__":
    main()
