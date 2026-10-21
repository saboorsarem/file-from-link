# 📥 File From Link

**Telegram-бот, превращающий ссылку в файл — с настоящей очередью, живым прогрессом и четырьмя языками интерфейса.**

[![Лицензия: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Telegram](https://img.shields.io/badge/Telegram-%40FileFromLinkBot-26A5E4?logo=telegram&logoColor=white)](https://t.me/FileFromLinkBot)
[![yt-dlp](https://img.shields.io/badge/powered%20by-yt--dlp-red)](https://github.com/yt-dlp/yt-dlp)
[![Языки](https://img.shields.io/badge/languages-EN%20%7C%20FA%20%7C%20RU%20%7C%20AR-8A2BE2)](#-языки)

[English](README.md) · [فارسی](README.fa.md) · **Русский** · [العربية](README.ar.md)

Скачивайте видео и аудио с **более чем 1700 сайтов** — YouTube, Instagram,
TikTok, X, SoundCloud, Vimeo и всего остального, что поддерживает
[yt-dlp](https://github.com/yt-dlp/yt-dlp). Отправьте ссылку, выберите качество
и получите файл прямо в чат.

## ✨ Возможности

| | Возможность |
|---|---|
| 🎚️ | **Выбор качества** — лучшее, 720p, 480p или только звук (MP3) в чате |
| 🌐 | **Четыре языка** — английский, персидский, русский, арабский; выбор один раз через `/language` |
| 🚦 | **Честная очередь** — Redis + RQ, пользователь видит свою позицию |
| 📊 | **Живой прогресс** — сообщение статуса обновляется по ходу загрузки |
| 🧯 | **Лимиты на пользователя** — 3 активные задачи по умолчанию, таймаут 30 минут |
| 📦 | **Большие файлы** — сверх 50 МБ Telegram отдаётся подписанная ссылка S3 или ссылка на своём сервере |
| 🍪 | **Cookies YouTube** — необязательный файл cookies для проверки «вы не робот» |
| 🧩 | **Два фронта, один движок** — бот на EC2 (long-polling) или Telegram Serverless, общий API `/jobs` |
| 🐳 | **Установка одной командой** — Docker Compose поднимает бота, API, worker, Redis и PO-token sidecar |

## 🏗️ Архитектура

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

**Почему не только Serverless?** Telegram Serverless исполняет обычный JS
в изоляте V8: без Python, npm-пакетов и ffmpeg, а ответы fetch ограничены
30 МБ ([документация](https://core.telegram.org/bots/serverless)). yt-dlp там
работать не может, поэтому Serverless — лишь необязательный мгновенный
фронтенд, а всё скачивание идёт на EC2.

## 🚀 Быстрый старт (EC2, режим A)

```bash
git clone https://github.com/saboorsarem/file-from-link.git
cd file-from-link
cp .env.example .env   # заполните BOT_TOKEN и API_SECRET
docker compose up -d --build
docker compose logs -f bot worker
```

Создать бота и получить `BOT_TOKEN` — через [@BotFather](https://t.me/BotFather),
см. [BOTFATHER.md](BOTFATHER.md). Полное пошаговое руководство (аккаунт AWS →
EC2 → Security Group → HTTPS → режим Serverless) — в
[персидском гайде](DEPLOY.fa.md).

## 🌐 Языки

Бот полностью переведён на четыре языка. Новый пользователь выбирает язык
кнопками; выбор сохраняется для него, и все сообщения — приветствие, выбор
качества, позиция в очереди, прогресс, ошибки и доставка — приходят на этом
языке. Сменить можно в любой момент командой `/language`.

| Код | Язык | Флаг |
|---|---|---|
| `en` | Английский | 🇬🇧 |
| `fa` | Персидский (فارسی) | 🇮🇷 |
| `ru` | Русский | 🇷🇺 |
| `ar` | Арабский (العربية) | 🇸🇦 |

Файлы переводов: [`app/i18n.py`](app/i18n.py) для бота и worker на EC2,
[`serverless/tgcloud/lib/i18n.js`](serverless/tgcloud/lib/i18n.js) для
необязательного фронта Serverless (берёт язык клиента Telegram).

## ⚙️ Настройки

Все параметры читаются из `.env` (пример: [`.env.example`](.env.example)):

| Переменная | По умолчанию | Назначение |
|---|---|---|
| `BOT_TOKEN` | — | Токен бота Telegram (обязательно) |
| `API_SECRET` | `change-me` | Общий секрет API `/jobs` |
| `PUBLIC_BASE_URL` | — | Публичный HTTPS-адрес для ссылок на большие файлы |
| `S3_BUCKET` / `AWS_REGION` | — | Доставка через S3 для файлов больше 50 МБ |
| `MAX_JOBS_PER_USER` | `3` | Одновременные задачи на пользователя |
| `JOB_TIMEOUT_SECONDS` | `1800` | Жёсткий лимит на одну загрузку |
| `FILE_TTL_HOURS` | `24` | Срок жизни ссылок на файлы |
| `YTDLP_COOKIES_FILE` | — | Необязательные cookies для проверок YouTube |
| `REDIS_URL` / `DATABASE_PATH` | значения compose | Очередь и история задач |

## ⚠️ Ограничения

- Боты загружают не больше **50 МБ** на файл — всё крупнее отдаётся ссылкой.
- Некоторые сайты (особенно YouTube с IP дата-центров) требуют cookies или
  ограничивают скорость; помогают `YTDLP_COOKIES_FILE` и встроенный
  PO-token sidecar.
- Это форк проекта
  [rzashakeri/file-from-link](https://github.com/rzashakeri/file-from-link)
  с добавленными русским и арабским переводами и обновлённой документацией.

## 📄 Лицензия

[MIT](LICENSE) © Reza Shakeri и участники.
