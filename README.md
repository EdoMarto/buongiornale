<p align="center">
  <img src="docs/logo.png" alt="Buongiornale" width="200">
</p>

<h1 align="center">Buongiornale</h1>

<p align="center">The day's news from major outlets' RSS feeds, posted to a Telegram channel.</p>

---

Buongiornale reads the RSS feeds of major Italian news outlets, removes duplicates, and posts the news
to a Telegram channel — like [@BuonGiornale](https://t.me/BuonGiornale). There is no web frontend: the
Telegram channel *is* the newspaper.

## Two modes

- **`digest`** — a morning roundup: the last 24 hours grouped by section (front page, economy, tech) in
  one message. Run once a day.
- **`stream`** — posts each new article as it appears, one per message. Run often; it remembers what it
  already sent and never reposts.

## Setup

Requires Python 3.10+.

```bash
pip install -r requirements.txt
cp .env.example .env      # then fill it in
```

1. Create a bot with [@BotFather](https://t.me/BotFather) → `TELEGRAM_BOT_TOKEN`.
2. Add the bot as an **admin** of your channel.
3. Put the channel in `TELEGRAM_CHANNEL` (e.g. `@BuonGiornale`).

## Run

```bash
python -m buongiornale digest --dry-run   # print the roundup, don't post
python -m buongiornale digest             # post the morning roundup
python -m buongiornale stream             # post new articles since the last run
```

Without the Telegram variables set, it prints instead of posting.

Schedule it with cron (or Windows Task Scheduler), e.g. the digest every morning:

```cron
0 7 * * * cd /path/to/buongiornale && /path/to/python -m buongiornale digest
```

## Feeds

Outlets live in [`feeds.json`](feeds.json), each with a source and a category. Add one with a line:

```json
{ "source": "Il Post", "category": "Front page", "url": "https://www.ilpost.it/feed/" }
```

It posts the title, outlet and a link to the original article — never the full text.

## Tests

```bash
pytest
```

## Tech stack

Python · feedparser · Telegram Bot API · SQLite

## License

[MIT](LICENSE)
