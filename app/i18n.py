"""UI strings in English, Persian, Russian and Arabic.

The user picks a language once via inline buttons; it is stored in the DB and
every bot/worker message uses it. Add a language by copying a dict - keys must
stay identical across languages."""
LANGUAGES = {
    "en": "🇬🇧 English",
    "fa": "🇮🇷 فارسی",
    "ru": "🇷🇺 Русский",
    "ar": "🇸🇦 العربية",
}
DEFAULT_LANG = "en"
STRINGS = {
    "en": {
        "choose_language": "🌐 Choose your language:\nEnglish · فارسی · Русский · العربية",
        "language_button": "🌐 Language",
        "welcome": "📥 File From Link — send a link, get a file!\nSend me a video link (YouTube, Instagram, TikTok, X and 1,700+ sites), pick a quality, and the file lands right here. When it is busy, jobs wait in a fair queue.",
        "no_url": "I could not find a link in that message. Send a full URL.",
        "quality_question": "🎬 {url}\nWhich quality should I download?",
        "fmt_best": "🎬 Best quality", "fmt_720": "📺 720p", "fmt_480": "📺 480p", "fmt_audio": "🎵 Audio only (MP3)",
        "queued_adding": "⏳ Adding you to the queue…",
        "queued": "⏳ You are in the queue — position: {pos}\nJob ID: {jid}",
        "queue_full": "🚦 Your queue is full. Wait for your current jobs to finish.",
        "expired": "⏰ That request expired — send the link again.",
        "downloading": "⬇️ Downloading… {pct}%",
        "uploading": "⬆️ Sending to Telegram…",
        "done": "✅ Done: {title}",
        "failed": "❌ Download failed:\n{error}",
        "failed_generic": "❌ Something went wrong while downloading. Please try again.",
        "too_big": "📦 “{title}” is bigger than Telegram's 50MB bot limit ({mb}MB).\nDownload link (valid {hours}h):\n{url}",
        "language_set": "✅ Language set to English. Send me a link whenever you are ready!",
    },
    "fa": {
        "choose_language": "🌐 زبان خود را انتخاب کنید:\nEnglish · فارسی · Русский · العربية",
        "language_button": "🌐 زبان",
        "welcome": "📥 فایل از لینک — لینک بفرست، فایل بگیر!\nلینک ویدیو رو بفرست (یوتیوب، اینستاگرام، تیک‌تاک، X و ۱۷۰۰+ سایت)، کیفیت رو انتخاب کن و فایل رو همینجا تحویل بگیر. وقتی شلوغ باشه، کارها به نوبت توی صف می‌رن.",
        "no_url": "توی این پیام لینکی پیدا نکردم. یک URL کامل بفرست.",
        "quality_question": "🎬 {url}\nبا چه کیفیتی دانلود کنم؟",
        "fmt_best": "🎬 بهترین کیفیت", "fmt_720": "📺 720p", "fmt_480": "📺 480p", "fmt_audio": "🎵 فقط صدا (MP3)",
        "queued_adding": "⏳ در حال اضافه کردن به صف…",
        "queued": "⏳ توی صف هستی — نوبت: {pos}\nشناسه کار: {jid}",
        "queue_full": "🚦 صف تو پره. صبر کن کارهای قبلی تموم بشن.",
        "expired": "⏰ این درخواست منقضی شده — لینک رو دوباره بفرست.",
        "downloading": "⬇️ در حال دانلود… {pct}٪",
        "uploading": "⬆️ در حال ارسال به تلگرام…",
        "done": "✅ انجام شد: {title}",
        "failed": "❌ دانلود ناموفق بود:\n{error}",
        "failed_generic": "❌ خطای غیرمنتظره هنگام دانلود. دوباره تلاش کن.",
        "too_big": "📦 «{title}» بزرگ‌تر از سقف ۵۰MB تلگرام است ({mb}MB).\nلینک دانلود ({hours} ساعت معتبر):\n{url}",
        "language_set": "✅ زبان فارسی شد. هر وقت آماده‌ای لینک بفرست!",
    },
    "ru": {
        "choose_language": "🌐 Выберите язык:\nEnglish · فارسی · Русский · العربية",
        "language_button": "🌐 Язык",
        "welcome": "📥 File From Link — отправьте ссылку, получите файл!\nПришлите ссылку на видео (YouTube, Instagram, TikTok, X и более 1700 сайтов), выберите качество — и файл придёт сюда. Если сервер занят, задачи ждут в очереди.",
        "no_url": "В этом сообщении нет ссылки. Отправьте полный URL.",
        "quality_question": "🎬 {url}\nВ каком качестве скачать?",
        "fmt_best": "🎬 Лучшее качество", "fmt_720": "📺 720p", "fmt_480": "📺 480p", "fmt_audio": "🎵 Только звук (MP3)",
        "queued_adding": "⏳ Добавляю вас в очередь…",
        "queued": "⏳ Вы в очереди — позиция: {pos}\nID задачи: {jid}",
        "queue_full": "🚦 Ваша очередь заполнена. Дождитесь окончания текущих задач.",
        "expired": "⏰ Запрос устарел — отправьте ссылку ещё раз.",
        "downloading": "⬇️ Скачиваю… {pct}%",
        "uploading": "⬆️ Отправляю в Telegram…",
        "done": "✅ Готово: {title}",
        "failed": "❌ Ошибка загрузки:\n{error}",
        "failed_generic": "❌ Что-то пошло не так при загрузке. Попробуйте ещё раз.",
        "too_big": "📦 «{title}» больше лимита Telegram в 50 МБ ({mb} МБ).\nСсылка на скачивание (действует {hours} ч):\n{url}",
        "language_set": "✅ Язык переключён на русский. Отправьте ссылку, когда будете готовы!",
    },
    "ar": {
        "choose_language": "🌐 اختر لغتك:\nEnglish · فارسی · Русский · العربية",
        "language_button": "🌐 اللغة",
        "welcome": "📥 File From Link — أرسل رابطًا واحصل على ملف!\nأرسل رابط فيديو (YouTube وInstagram وTikTok وX وأكثر من 1700 موقع)، واختر الجودة، وسيصل الملف إلى هنا. وعند الازدحام تنتظر المهام في قائمة عادلة.",
        "no_url": "لم أجد رابطًا في هذه الرسالة. أرسل عنوان URL كاملًا.",
        "quality_question": "🎬 {url}\nبأي جودة أحمّل؟",
        "fmt_best": "🎬 أفضل جودة", "fmt_720": "📺 720p", "fmt_480": "📺 480p", "fmt_audio": "🎵 صوت فقط (MP3)",
        "queued_adding": "⏳ جارٍ إضافتك إلى قائمة الانتظار…",
        "queued": "⏳ أنت في قائمة الانتظار — الترتيب: {pos}\nمعرّف المهمة: {jid}",
        "queue_full": "🚦 قائمتك ممتلئة. انتظر انتهاء مهامك الحالية.",
        "expired": "⏰ انتهت صلاحية هذا الطلب — أرسل الرابط مرة أخرى.",
        "downloading": "⬇️ جارٍ التنزيل… {pct}%",
        "uploading": "⬆️ جارٍ الإرسال إلى Telegram…",
        "done": "✅ تم: {title}",
        "failed": "❌ فشل التنزيل:\n{error}",
        "failed_generic": "❌ حدث خطأ غير متوقع أثناء التنزيل. حاول مرة أخرى.",
        "too_big": "📦 «{title}» أكبر من حدّ تلغرام 50 ميجابايت ({mb} ميجابايت).\nرابط التنزيل (صالح لمدة {hours} ساعة):\n{url}",
        "language_set": "✅ تم تعيين اللغة إلى العربية. أرسل رابطًا عندما تكون جاهزًا!",
    },
}
def t(lang: str, key: str, **kw) -> str:
    s = STRINGS.get(lang, STRINGS[DEFAULT_LANG]).get(key) or STRINGS[DEFAULT_LANG][key]
    return s.format(**kw) if kw else s
def fmt_label(lang: str, choice: str) -> str:
    return t(lang, f"fmt_{choice}")
