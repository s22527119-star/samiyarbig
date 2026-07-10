# Rubika GPT Bot

یک ربات ساده برای اتصال پیام‌های روبیکا به مدل‌های OpenAI.

## امکانات
- دریافت پیام از وبهوک روبیکا
- ارسال پیام کاربر به OpenAI
- تولید پاسخ فارسی
- ارسال پاسخ به روبیکا (تابع ارسال در این نسخه به‌صورت placeholder است)

## نصب
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## اجرا
```bash
export $(cat .env | xargs)
python bot.py
```

سرویس روی آدرس زیر بالا می‌آید:
- `GET /health`
- `POST /webhook`

## نمونه payload وبهوک
```json
{
  "chat_id": "u0abc123",
  "text": "سلام، حالت چطوره؟"
}
```

## اتصال واقعی به روبیکا
در فایل `bot.py` تابع `send_message_to_rubika` را با API رسمی ربات روبیکا جایگزین کن.
در حال حاضر برای جلوگیری از خطا، این تابع پیام را در خروجی چاپ می‌کند.

## نکات امنیتی
- کلید `OPENAI_API_KEY` را داخل کد hardcode نکن.
- دسترسی وبهوک را با IP allowlist یا امضای درخواست امن کن.
