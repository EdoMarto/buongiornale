<p align="center">
  <img src="docs/logo.png" alt="Buongiornale" width="200">
</p>

<h1 align="center">Buongiornale</h1>

<p align="center">The day's news from the main outlets' RSS feeds, posted to a Telegram channel.</p>

Buongiornale reads the RSS feeds of the main Italian news outlets, drops the duplicates, and posts the
news to a Telegram channel, like [@BuonGiornale](https://t.me/BuonGiornale). There's no website: the
Telegram channel is the newspaper.

## Two modes

* `digest` is the morning roundup. It takes the last 24 hours, groups them by section (front page,
  economy, tech) and sends it as one message. Run it once a day.
* `stream` posts each new article as it shows up, one per message. Run it often; it remembers what it
  already sent, so nothing goes out twice.

## Setup

You need Python 3.10 or newer.

```bash
pip install -r requirements.txt
cp .env.example .env      # then fill it in
```

1. Create a bot with [@BotFather](https://t.me/BotFather) and copy the token into `TELEGRAM_BOT_TOKEN`.
2. Add the bot to your channel as an admin so it can post.
3. Put the channel in `TELEGRAM_CHANNEL`, for example `@BuonGiornale`.

## Run

```bash
python -m buongiornale digest --dry-run   # print the roundup, don't post
python -m buongiornale digest             # post the morning roundup
python -m buongiornale stream             # post new articles since the last run
```

If the Telegram variables aren't set, it just prints instead of posting.

Run it on a schedule with cron (or Windows Task Scheduler). For example, the digest every morning:

```cron
0 7 * * * cd /path/to/buongiornale && /path/to/python -m buongiornale digest
```

## Feeds

The outlets live in [`feeds.json`](feeds.json), each with a source and a category. Adding one is a single
line:

```json
{ "source": "Il Post", "category": "Front page", "url": "https://www.ilpost.it/feed/" }
```

It only posts the title, the outlet and a link to the original article, never the full text.

## Tests

```bash
pytest
```

## Built with

Python, feedparser and the Telegram Bot API.

## License

[MIT](LICENSE)
