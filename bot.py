from telegram.ext import Updater, MessageHandler, Filters
from telegram import Bot
import pytesseract
from PIL import Image
from io import BytesIO

# 🔧 مسیر نصب Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 🧠 تابع پردازش عکس و استخراج متن با تنظیمات دقیق
def handle_image(update, context):
    photo = update.message.photo[-1]
    file = photo.get_file()
    image_bytes = file.download_as_bytearray()
    image = Image.open(BytesIO(image_bytes))

    try:
        # 🎯 تنظیمات دقیق برای Tesseract
        custom_config = r'--oem 3 --psm 6' # Engine mode 3 = default + LSTM, PSM 6 = Assume a single uniform block of text

        # 🌐 استخراج متن فارسی و انگلیسی
        text = pytesseract.image_to_string(image, lang='eng+fas', config=custom_config)

        if text.strip():
            update.message.reply_text("📝 متن استخراج‌شده:\n" + text)
        else:
            update.message.reply_text("❗ متنی در عکس پیدا نشد.")
    except Exception as e:
        update.message.reply_text(f"❌ خطا در پردازش عکس:\n{str(e)}")

# 🧩 تابع اصلی راه‌اندازی ربات
def main():
    # توکن ربات خودتو اینجا بذار
    TOKEN = '7816623288:AAFvHywexRItI2M1B7fA8dom6frrh4tKhFM'

    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.photo, handle_image))

    print("🤖 ربات فعال شد...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
