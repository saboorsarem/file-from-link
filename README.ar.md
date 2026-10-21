# 📥 File From Link

**بوت تلغرام يحوّل الرابط إلى ملف — بقائمة انتظار حقيقية وتقدّم مباشر وواجهة بأربع لغات.**

[![الرخصة: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Telegram](https://img.shields.io/badge/Telegram-%40FileFromLinkBot-26A5E4?logo=telegram&logoColor=white)](https://t.me/FileFromLinkBot)
[![yt-dlp](https://img.shields.io/badge/powered%20by-yt--dlp-red)](https://github.com/yt-dlp/yt-dlp)
[![اللغات](https://img.shields.io/badge/languages-EN%20%7C%20FA%20%7C%20RU%20%7C%20AR-8A2BE2)](#-اللغات)

[English](README.md) · [فارسی](README.fa.md) · [Русский](README.ru.md) · **العربية**

نزّل الفيديو والصوت من **أكثر من 1700 موقع** — يوتيوب، إنستغرام، تيك توك،
إكس، ساوند كلاود، فيميو وكل ما يدعمه
[yt-dlp](https://github.com/yt-dlp/yt-dlp). أرسل الرابط، اختر الجودة، واستلم
الملف في المحادثة نفسها.

## ✨ المزايا

| | الميزة |
|---|---|
| 🎚️ | **اختيار الجودة** — أفضل جودة أو 720p أو 480p أو صوت فقط (MP3) داخل المحادثة |
| 🌐 | **أربع لغات** — الإنجليزية والفارسية والروسية والعربية؛ تُختار مرة واحدة عبر `/language` |
| 🚦 | **قائمة انتظار عادلة** — Redis + RQ، ويرى المستخدم ترتيبه |
| 📊 | **تقدّم مباشر** — تُحدَّث رسالة الحالة مع تقدّم التنزيل |
| 🧯 | **حدود لكل مستخدم** — 3 مهام نشطة افتراضيًا، ومهلة 30 دقيقة للمهمة |
| 📦 | **الملفات الكبيرة** — فوق حد تلغرام 50 ميجابايت يصلك رابط S3 موقّع أو رابط من خادمك |
| 🍪 | **ملفات تعريف يوتيوب** — ملف cookies اختياري لتجاوز «تأكيد أنك لست روبوتًا» |
| 🧩 | **واجهتان ومحرّك واحد** — بوت EC2 بنمط long-polling أو Telegram Serverless، وبواجهة `/jobs` مشتركة |
| 🐳 | **نشر بأمر واحد** — Docker Compose يشغّل البوت وAPI وworker وRedis وخدمة PO-token |

## 🏗️ البنية

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

**لماذا لا يكفي Serverless وحده؟** يشغّل Telegram Serverless جافاسكربت عاديًا
داخل V8 isolate: بلا Python ولا حزم npm ولا ffmpeg، وبحد أقصى 30 ميجابايت
لردود fetch ([التوثيق](https://core.telegram.org/bots/serverless)). لا يمكن
تشغيل yt-dlp هناك؛ لذلك Serverless واجهة سريعة اختيارية فقط، وكل التنزيل
يحدث على EC2.

## 🚀 البداية السريعة (EC2، النمط A)

```bash
git clone https://github.com/saboorsarem/file-from-link.git
cd file-from-link
cp .env.example .env   # املأ BOT_TOKEN و API_SECRET
docker compose up -d --build
docker compose logs -f bot worker
```

أنشئ البوت واحصل على `BOT_TOKEN` عبر [@BotFather](https://t.me/BotFather) —
انظر [BOTFATHER.md](BOTFATHER.md). الدليل الكامل خطوة بخطوة (حساب AWS →
EC2 → Security Group → HTTPS → نمط Serverless) في
[الدليل الفارسي](DEPLOY.fa.md).

## 🌐 اللغات

يأتي البوت بترجمة كاملة لأربع لغات. يختار المستخدم الجديد لغته بالأزرار،
ويُحفَظ اختياره، وكل الرسائل — الترحيب، اختيار الجودة، ترتيب الانتظار،
التقدّم، الأخطاء، وتسليم الملف — تصله بهذه اللغة. يمكن التغيير في أي وقت
بأمر `/language`.

| الرمز | اللغة | العلم |
|---|---|---|
| `en` | الإنجليزية | 🇬🇧 |
| `fa` | الفارسية (فارسی) | 🇮🇷 |
| `ru` | الروسية (Русский) | 🇷🇺 |
| `ar` | العربية | 🇸🇦 |

ملفات الترجمة: [`app/i18n.py`](app/i18n.py) لبوت EC2 وworker، و
[`serverless/tgcloud/lib/i18n.js`](serverless/tgcloud/lib/i18n.js) لواجهة
Serverless الاختيارية (تتبع لغة تطبيق تلغرام).

## ⚙️ الإعدادات

كل الإعدادات تُقرأ من `.env` (نموذج: [`.env.example`](.env.example)):

| المتغيّر | الافتراضي | الغرض |
|---|---|---|
| `BOT_TOKEN` | — | رمز بوت تلغرام (مطلوب) |
| `API_SECRET` | `change-me` | السر المشترك لواجهة `/jobs` |
| `PUBLIC_BASE_URL` | — | عنوان HTTPS عام لروابط الملفات الكبيرة |
| `S3_BUCKET` / `AWS_REGION` | — | التسليم عبر S3 للملفات فوق 50 ميجابايت |
| `MAX_JOBS_PER_USER` | `3` | المهام المتزامنة لكل مستخدم |
| `JOB_TIMEOUT_SECONDS` | `1800` | الحد الأقصى لزمن التنزيل الواحد |
| `FILE_TTL_HOURS` | `24` | مدة صلاحية روابط التنزيل |
| `YTDLP_COOKIES_FILE` | — | ملف cookies اختياري لفحوص يوتيوب |
| `REDIS_URL` / `DATABASE_PATH` | إعدادات compose | قائمة الانتظار وسجل المهام |

## ⚠️ القيود

- الحد الأقصى لما يرفعه البوت **50 ميجابايت** لكل ملف — وما زاد يُسلَّم كرابط.
- بعض المواقع (خصوصًا يوتيوب من عناوين مراكز البيانات) تطلب cookies أو تحدّ
  من السرعة؛ يساعد `YTDLP_COOKIES_FILE` وخدمة PO-token المرفقة.
- هذا المشروع نسخة (fork) من
  [rzashakeri/file-from-link](https://github.com/rzashakeri/file-from-link)
  مع إضافة الترجمتين الروسية والعربية وتحديث التوثيق.

## 📄 الرخصة

[MIT](LICENSE) © Reza Shakeri والمساهمون.
