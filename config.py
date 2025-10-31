import os
from dotenv import load_dotenv

load_dotenv()

# إعدادات تيليجرام
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_APP_ID = os.getenv("TELEGRAM_APP_ID", "")

# إعدادات البوت
UPDATE_INTERVAL = 60  # تحديث كل دقيقة
MAX_RETRIES = 3
PREDICTION_ACCURACY = 85  # دقة التوقع %

# روابط مباشرة لـ 1xbet
XBET_LIVE_URL = "https://1xbet.com/en/live"
XBET_SPORTS_URL = "https://1xbet.com/en/sports"