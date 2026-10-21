# 📥 File From Link

**A Telegram bot that turns a link into a file — with a real job queue, live progress and four UI languages.**

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Telegram](https://img.shields.io/badge/Telegram-%40FileFromLinkBot-26A5E4?logo=telegram&logoColor=white)](https://t.me/FileFromLinkBot)
[![yt-dlp](https://img.shields.io/badge/powered%20by-yt--dlp-red)](https://github.com/yt-dlp/yt-dlp)
[![Languages](https://img.shields.io/badge/languages-EN%20%7C%20FA%20%7C%20RU%20%7C%20AR-8A2BE2)](#-languages)

**English** · [فارسی](README.fa.md) · [Русский](README.ru.md) · [العربية](README.ar.md)

Download videos and audio from **1,700+ sites** — YouTube, Instagram, TikTok, X,
SoundCloud, Vimeo and everything else [yt-dlp](https://github.com/yt-dlp/yt-dlp)
supports. Send a link, pick a quality, get the file back in the chat.

## ✨ Features

| | Feature |
|---|---|
| 🎚️ | **Quality picker** — Best, 720p, 480p or audio-only MP3, right in the chat |
| 🌐 | **Four languages** — English, Persian, Russian, Arabic; chosen once with `/language` |
| 🚦 | **Fair queue** — Redis + RQ, users see their position, no silent waiting |
| 📊 | **Live progress** — the status message is edited as the download advances |
| 🧯 | **Per-user limits** — 3 active jobs by default, 30-minute job timeout |
| 📦 | **Large files** — above Telegram's 50 MB limit you get an S3 presigned or self-hosted link |
| 🍪 | **YouTube cookies** — optional cookie file for "confirm you're not a bot" |
| 🧩 | **Two fronts, one engine** — EC2 long-polling bot or Telegram Serverless, same `/jobs` API |
| 🐳 | **One-command deploy** — Docker Compose brings up bot, API, worker, Redis and PO-token sidecar |

## 🏗️ Architecture

```
                 ┌──────────────────────────────────────────────┐
 Link in chat ──►│ Front (pick ONE)                             │
                 │  A) app/bot.py on EC2 (long-polling) [default]│
                 │  B) serverless/ Telegram Serverless (V8)     │
                 └───────────────┬──────────────────────────────┘
                                 │ POST /jobs  (X-API-Secret)
                                 ▼
                 ┌──────────────────────────────────────────────┐
                 │ EC2 engine                                   │
                 │  FastAPI (app/api.py) ─► Redis queue (RQ)    │
                 │  Workers (app/worker.py, scalable)           │
                 │    └► yt-dlp + ffmpeg ─► file                │
                 │         ├─ ≤49MB ─► sendVideo/sendDocument   │
                 │         └─ >49MB ─► S3 presigned link         │
                 │                    or /files/<token>/ link   │
                 └──────────────────────────────────────────────┘
```

**Why not Serverless-only?** Telegram Serverless runs plain JS in a V8 isolate:
no Python, no npm packages, no ffmpeg, and fetch responses are capped at 30 MB
([docs](https://core.telegram.org/bots/serverless)). yt-dlp *cannot* run there,
so Serverless is only an optional instant front-end while all downloading
happens on EC2.

## 🚀 Quick start (EC2, Mode A)

```bash
git clone https://github.com/saboorsarem/file-from-link.git
cd file-from-link
cp .env.example .env   # set BOT_TOKEN and API_SECRET
docker compose up -d --build
docker compose logs -f bot worker
```

Create the bot and get `BOT_TOKEN` with [@BotFather](https://t.me/BotFather) —
see [BOTFATHER.md](BOTFATHER.md). The full walkthrough (AWS account → EC2 →
security group → HTTPS → Serverless mode) is in the
[Persian deployment guide](DEPLOY.fa.md).

## 🌐 Languages

The bot ships with complete translations. A new user picks a language with
inline buttons; the choice is stored per user and every message — welcome,
quality picker, queue position, progress, errors, delivery — uses it.
Change it at any time with `/language`.

| Code | Language | Flag |
|---|---|---|
| `en` | English | 🇬🇧 |
| `fa` | Persian (فارسی) | 🇮🇷 |
| `ru` | Russian (Русский) | 🇷🇺 |
| `ar` | Arabic (العربية) | 🇸🇦 |

Translation files: [`app/i18n.py`](app/i18n.py) for the EC2 bot and worker,
[`serverless/tgcloud/lib/i18n.js`](serverless/tgcloud/lib/i18n.js) for the
optional Serverless front (it follows the Telegram client language).

## ⚙️ Configuration

All settings come from `.env` (see [`.env.example`](.env.example)):

| Variable | Default | Purpose |
|---|---|---|
| `BOT_TOKEN` | — | Telegram bot token (required) |
| `API_SECRET` | `change-me` | Shared secret for the `/jobs` API |
| `PUBLIC_BASE_URL` | — | Public HTTPS address for large-file links |
| `S3_BUCKET` / `AWS_REGION` | — | S3 delivery for files over 50 MB |
| `MAX_JOBS_PER_USER` | `3` | Concurrent jobs per user |
| `JOB_TIMEOUT_SECONDS` | `1800` | Hard limit per download |
| `FILE_TTL_HOURS` | `24` | Lifetime of generated download links |
| `YTDLP_COOKIES_FILE` | — | Optional cookies for YouTube bot checks |
| `REDIS_URL` / `DATABASE_PATH` | compose defaults | Queue and job history |

## ⚠️ Limits

- Bots can upload **50 MB** per file — bigger results are delivered as links.
- Some sites (YouTube from datacenter IPs in particular) require cookies or
  rate-limit downloads; `YTDLP_COOKIES_FILE` and the bundled PO-token sidecar
  help.
- This project is a fork of
  [rzashakeri/file-from-link](https://github.com/rzashakeri/file-from-link),
  extended with Russian and Arabic localization and refreshed documentation.

## 📄 License

[MIT](LICENSE) © Reza Shakeri and contributors.
