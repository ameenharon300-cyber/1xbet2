import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from config import TELEGRAM_BOT_TOKEN
from prediction_engine import PredictionEngine

# إعداد التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class GoalPredictionBot:
    def __init__(self):
        self.application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        self.prediction_engine = PredictionEngine()
        self.setup_handlers()
        
    def setup_handlers(self):
        """إعداد معالجات الأوامر"""
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("goal", self.goal_prediction))
        self.application.add_handler(CommandHandler("next", self.next_prediction))
        self.application.add_handler(CommandHandler("stats", self.stats_command))
        
    async def start_command(self, update: Update, context: CallbackContext):
        """أمر البدء"""
        user = update.effective_user
        welcome_message = f"""
🎯 **مرحباً {user.first_name}!**

أنا بوت توقعات **GOAL / NO GOAL** المتقدم ⚽

**كيفية العمل:**
- أرسل /goal للحصول على توقع الهدف الحالي
- أرسل /next للتوقع القادم  
- أرسل /stats لإحصائيات التوقعات

⚡ **مميزات البوت:**
✅ تحديث مباشر من 1xbet
🎯 دقة تصل إلى 85%
📊 تحليل حي للمباريات
🕒 تحديث كل دقيقة

**استخدم /goal الآن!**
        """
        await update.message.reply_text(welcome_message, parse_mode='Markdown')
        
    async def goal_prediction(self, update: Update, context: CallbackContext):
        """توقع الهدف الحالي"""
        try:
            await update.message.reply_text("🎯 جاري تحليل المباراة الحالية...")
            
            # جلب التوقع من المحرك
            prediction = await self.prediction_engine.get_goal_prediction()
            
            if prediction["status"] == "success":
                response = f"""
⚽ **توقع الهدف الحالي:**

🏆 **المباراة:** {prediction['match']}
⏰ **الوقت:** {prediction['time']}
🎯 **التوقع:** **{prediction['prediction']}**
📊 **الثقة:** {prediction['confidence']}%
🔴 **النتيجة الحالية:** {prediction['score']}

💡 **تحليل:** {prediction['analysis']}

🔄 أرسل /next للتوقع القادم
                """
            else:
                response = "⚠️ لا توجد مباريات حية حالياً. حاول لاحقاً!"
                
            await update.message.reply_text(response, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error in goal prediction: {e}")
            await update.message.reply_text("❌ حدث خطأ في جلب التوقع")
            
    async def next_prediction(self, update: Update, context: CallbackContext):
        """التوقع القادم"""
        try:
            await update.message.reply_text("🔮 جاري تحليل التوقعات القادمة...")
            
            prediction = await self.prediction_engine.get_next_prediction()
            
            response = f"""
🔮 **التوقع القادم:**

🏆 **المباراة:** {prediction['match']}
🕒 **الموعد:** {prediction['schedule']}
🎯 **التوقع:** **{prediction['prediction']}**
📈 **احتمالية الهدف:** {prediction['goal_probability']}%
⭐ **مستوى الثقة:** {prediction['confidence']}

💎 **النصيحة:** {prediction['advice']}

⚡ أرسل /goal للتوقع الحالي
            """
            
            await update.message.reply_text(response, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error in next prediction: {e}")
            await update.message.reply_text("❌ حدث خطأ في جلب التوقع القادم")
        
    async def stats_command(self, update: Update, context: CallbackContext):
        """إحصائيات التوقعات"""
        stats = await self.prediction_engine.get_stats()
        
        stats_message = f"""
📈 **إحصائيات التوقعات:**

✅ **التوقعات الصحيحة:** {stats['correct_predictions']}
❌ **التوقعات الخاطئة:** {stats['wrong_predictions']}
🎯 **معدل الدقة:** {stats['accuracy']}%
⚽ **إجمالي التوقعات:** {stats['total_predictions']}

🔥 **النسبة الحالية:** {stats['current_streak']} توقعات صحيحة متتالية

🕒 **آخر تحديث:** {stats['last_update']}
        """
        await update.message.reply_text(stats_message, parse_mode='Markdown')
        
    async def run(self):
        """تشغيل البوت"""
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()
        
        logger.info("🤖 بوت توقعات الهدف يعمل الآن!")
        
        # تشغيل التحديث التلقائي
        asyncio.create_task(self.prediction_engine.auto_update())
        
        # الحفاظ على البوت شغال
        await asyncio.Future()

if __name__ == "__main__":
    bot = GoalPredictionBot()
    asyncio.run(bot.run())