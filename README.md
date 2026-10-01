<p align="center">
  <img src="docs/logo.png" alt="Buongiornale" width="200">
</p>

<h1 align="center">Buongiornale</h1>

<p align="center">Le notizie del giorno dalle principali testate, raccolte dai feed RSS e pubblicate su un canale Telegram.</p>

---

Buongiornale legge i feed RSS delle principali testate italiane, mette insieme le notizie del giorno,
toglie i doppioni e le pubblica su un canale Telegram — come [@BuonGiornale](https://t.me/BuonGiornale).
Non ha interfaccia web: il canale Telegram *è* il giornale.

## Due modalità

- **`digest`** — la rassegna del mattino: le notizie delle ultime 24 ore raggruppate per sezione
  (Prima pagina, Economia, Tecnologia…) in un unico messaggio. Da lanciare una volta al giorno.
- **`stream`** — pubblica ogni nuovo articolo appena esce, uno per messaggio. Da lanciare spesso (es.
  ogni 15 minuti); ricorda cosa ha già inviato e non ripete.

### Esempio (modalità digest)

> 🗞 **Buongiornale** — giovedì 1 ottobre 2026
> Le notizie del giorno dalle principali testate.
>
> **🏛 Prima pagina**
> • [Conciliazione vita-lavoro, parte la certificazione per le aziende](#) — *Sky TG24*
> • [Guerra Ucraina, l'Assemblea del Consiglio d'Europa](#) — *Sky TG24*
>
> **💶 Economia**
> • [Istat: ad agosto la disoccupazione sale al 6,2%](#) — *Il Sole 24 Ore*
>
> **💻 Tecnologia**
> • [Apple risarcirà i proprietari di MacBook per le tastiere](#) — *ANSA Tecnologia*

## Come funziona

```
feeds.json ─► fetch (feedparser) ─► dedupe ─► filter last 24h ─► group by category ─► Telegram
                                                  │
                                          SQLite "seen" store (stream mode: no reposts)
```

- **`aggregator.py`** scarica i feed, li normalizza in `Article`, toglie i duplicati (per link e per
  titolo) e filtra le notizie recenti.
- **`formatter.py`** costruisce i messaggi in HTML, spezzandoli per restare sotto il limite di Telegram.
- **`store.py`** tiene traccia in SQLite di ciò che è già stato pubblicato (modalità `stream`).
- **`telegram.py`** invia messaggi e foto via Bot API.

## Testate

I feed sono in [`feeds.json`](feeds.json), ognuno con sorgente e categoria. Di default: ANSA,
Repubblica, Corriere della Sera, Sky TG24, Il Sole 24 Ore, Wired. Aggiungerne altre è una riga di JSON:

```json
{ "source": "Il Post", "category": "Prima pagina", "url": "https://www.ilpost.it/feed/" }
```

## Setup

Requisiti: Python 3.10+.

```bash
pip install -r requirements.txt
cp .env.example .env      # poi compilalo
```

1. Crea un bot con [@BotFather](https://t.me/BotFather) → `TELEGRAM_BOT_TOKEN`.
2. Crea il canale, aggiungi il bot come **amministratore** (può pubblicare).
3. Metti il canale in `TELEGRAM_CHANNEL` (es. `@BuonGiornale`).

## Uso

```bash
python -m buongiornale digest --dry-run    # mostra la rassegna senza pubblicare
python -m buongiornale digest              # pubblica la rassegna del mattino (con il logo)
python -m buongiornale stream              # pubblica i nuovi articoli dall'ultimo giro
```

Senza le variabili Telegram impostate, il bot passa automaticamente in modalità anteprima (`--dry-run`).

### Automazione

- **Rassegna del mattino** (Linux/macOS cron, ogni giorno alle 7:00):
  ```cron
  0 7 * * * cd /path/to/buongiornale && /path/to/python -m buongiornale digest
  ```
- **Stream** (ogni 15 minuti):
  ```cron
  */15 * * * * cd /path/to/buongiornale && /path/to/python -m buongiornale stream
  ```
- **Windows:** usa l'Utilità di pianificazione con gli stessi comandi.

## Test

```bash
pytest
```

## Note

- Rispetta i termini d'uso dei feed: Buongiornale pubblica **titolo, testata e link** all'articolo
  originale, non il testo completo. Il traffico resta alle testate.
- Alcune testate bloccano le richieste automatiche o cambiano gli URL dei feed: adatta `feeds.json` di
  conseguenza.

## Tech stack

Python · feedparser · Telegram Bot API · SQLite

## Licenza

[MIT](LICENSE)
