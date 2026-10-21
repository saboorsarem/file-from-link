# 📥 فایل از لینک

**یک ربات تلگرام که لینک را به فایل تبدیل می‌کند — با صف واقعی، پیشرفت زنده و رابط کاربری چهار زبانه.**

[![مجوز: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Telegram](https://img.shields.io/badge/Telegram-%40FileFromLinkBot-26A5E4?logo=telegram&logoColor=white)](https://t.me/FileFromLinkBot)
[![yt-dlp](https://img.shields.io/badge/powered%20by-yt--dlp-red)](https://github.com/yt-dlp/yt-dlp)
[![زبان‌ها](https://img.shields.io/badge/languages-EN%20%7C%20FA%20%7C%20RU%20%7C%20AR-8A2BE2)](#-زبان‌ها)

[English](README.md) · **فارسی** · [Русский](README.ru.md) · [العربية](README.ar.md)

ویدیو و صدا را از **بیش از ۱۷۰۰ سایت** دانلود کنید — یوتیوب، اینستاگرام،
تیک‌تاک، X، ساندکلاد، ویمئو و هر چیزی که [yt-dlp](https://github.com/yt-dlp/yt-dlp)
پشتیبانی می‌کند. لینک را بفرستید، کیفیت را انتخاب کنید و فایل را در همان چت
تحویل بگیرید.

## ✨ امکانات

| | ویژگی |
|---|---|
| 🎚️ | **انتخاب کیفیت** — بهترین کیفیت، 720p، 480p یا فقط صدا (MP3) در خود چت |
| 🌐 | **چهار زبان** — انگلیسی، فارسی، روسی و عربی؛ انتخاب یک‌باره با `/language` |
| 🚦 | **صف منصفانه** — Redis + RQ، نمایش نوبت کاربر، بدون انتظار بی‌خبر |
| 📊 | **پیشرفت زنده** — پیام وضعیت همراه با پیشرفت دانلود ویرایش می‌شود |
| 🧯 | **محدودیت هر کاربر** — به‌طور پیش‌فرض ۳ کار فعال و مهلت ۳۰ دقیقه برای هر کار |
| 📦 | **فایل‌های بزرگ** — بیشتر از سقف ۵۰ مگابایت تلگرام، لینک S3 یا لینک موقت خود میزبان |
| 🍪 | **کوکی یوتیوب** — فایل کوکی اختیاری برای عبور از «ربات نیستم» |
| 🧩 | **دو رابط، یک موتور** — ربات EC2 با long-polling یا Telegram Serverless با API مشترک `/jobs` |
| 🐳 | **نصب با یک دستور** — Docker Compose ربات، API، worker، Redis و سایدکار PO-token را بالا می‌آورد |

## 🏗️ معماری

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

**چرا فقط Serverless کافی نیست؟** Telegram Serverless فقط جاوااسکریپت را در
یک V8 isolate اجرا می‌کند: نه پایتون، نه پکیج npm، نه ffmpeg، و پاسخ fetch
حداکثر ۳۰ مگابایت است
([مستندات](https://core.telegram.org/bots/serverless)). yt-dlp روی آن اجرا
نمی‌شود؛ پس Serverless فقط یک رابط سریع اختیاری است و همه دانلودها روی EC2
انجام می‌شوند.

## 🚀 شروع سریع (EC2، حالت A)

```bash
git clone https://github.com/saboorsarem/file-from-link.git
cd file-from-link
cp .env.example .env   # BOT_TOKEN و API_SECRET را پر کنید
docker compose up -d --build
docker compose logs -f bot worker
```

ساخت ربات و گرفتن `BOT_TOKEN` با [@BotFather](https://t.me/BotFather) — راهنما
در [BOTFATHER.md](BOTFATHER.md). راهنمای کامل قدم‌به‌قدم (حساب AWS → EC2 →
Security Group → HTTPS → حالت Serverless) در [DEPLOY.fa.md](DEPLOY.fa.md) است.

## 🌐 زبان‌ها

ربات ترجمه کامل هر چهار زبان را دارد. کاربر جدید زبان را با دکمه‌های شیشه‌ای
انتخاب می‌کند؛ انتخاب برای همان کاربر ذخیره می‌شود و همه پیام‌ها — خوش‌آمد،
انتخاب کیفیت، نوبت صف، پیشرفت، خطاها و تحویل فایل — با همان زبان نمایش داده
می‌شوند. هر وقت خواستید با `/language` تغییر دهید.

| کد | زبان | پرچم |
|---|---|---|
| `en` | انگلیسی | 🇬🇧 |
| `fa` | فارسی | 🇮🇷 |
| `ru` | روسی (Русский) | 🇷🇺 |
| `ar` | عربی (العربية) | 🇸🇦 |

فایل‌های ترجمه: [`app/i18n.py`](app/i18n.py) برای ربات EC2 و worker، و
[`serverless/tgcloud/lib/i18n.js`](serverless/tgcloud/lib/i18n.js) برای رابط
اختیاری Serverless (زبان را از تنظیمات تلگرام کاربر می‌خواند).

## ⚙️ تنظیمات

همه تنظیمات از `.env` خوانده می‌شوند (نمونه: [`.env.example`](.env.example)):

| متغیر | پیش‌فرض | کاربرد |
|---|---|---|
| `BOT_TOKEN` | — | توکن ربات تلگرام (الزامی) |
| `API_SECRET` | `change-me` | کلید مشترک API `/jobs` |
| `PUBLIC_BASE_URL` | — | آدرس HTTPS عمومی برای لینک فایل‌های بزرگ |
| `S3_BUCKET` / `AWS_REGION` | — | تحویل از S3 برای فایل‌های بیش از ۵۰ مگابایت |
| `MAX_JOBS_PER_USER` | `3` | تعداد کارهای هم‌زمان هر کاربر |
| `JOB_TIMEOUT_SECONDS` | `1800` | سقف زمانی هر دانلود |
| `FILE_TTL_HOURS` | `24` | مدت اعتبار لینک‌های دانلود |
| `YTDLP_COOKIES_FILE` | — | کوکی اختیاری برای بررسی ربات بودن یوتیوب |
| `REDIS_URL` / `DATABASE_PATH` | پیش‌فرض compose | صف و تاریخچه کارها |

## ⚠️ محدودیت‌ها

- ربات‌ها در هر فایل حداکثر **۵۰ مگابایت** می‌توانند آپلود کنند — نتیجه‌های
  بزرگ‌تر به‌صورت لینک تحویل داده می‌شوند.
- بعضی سایت‌ها (به‌ویژه یوتیوب از IP دیتاسنتر) کوکی می‌خواهند یا سرعت را محدود
  می‌کنند؛ `YTDLP_COOKIES_FILE` و سایدکار PO-token کمک می‌کنند.
- این پروژه فورکی از
  [rzashakeri/file-from-link](https://github.com/rzashakeri/file-from-link)
  است که با ترجمه روسی و عربی و مستندات به‌روز شده گسترش یافته.

## 📄 مجوز

[MIT](LICENSE) © رضا شاکری و مشارکت‌کنندگان.
