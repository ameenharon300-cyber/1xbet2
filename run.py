#!/usr/bin/env python3
import asyncio
import signal
import sys
from main_bot import GoalPredictionBot

class Application:
    def __init__(self):
        self.bot = None
        
    async def startup(self):
        """بدء التشغيل"""
        print("🚀 بدء تشغيل بوت توقعات الهدف...")
        self.bot = GoalPredictionBot()
        await self.bot.run()
        
    async def shutdown(self):
        """إيقاف التشغيل"""
        print("🛑 إيقاف البوت...")
        if self.bot:
            await self.bot.application.stop()
            await self.bot.application.shutdown()
            
def signal_handler(signum, frame):
    """معالج إشارات النظام"""
    print(f"📡 تم استقبال إشارة {signum}")
    asyncio.create_task(app.shutdown())
    sys.exit(0)

if __name__ == "__main__":
    app = Application()
    
    # تسجيل معالج الإشارات
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        asyncio.run(app.startup())
    except KeyboardInterrupt:
        print("⏹️ تم إيقاف البوت بواسطة المستخدم")
    except Exception as e:
        print(f"❌ خطأ غير متوقع: {e}")
    finally:
        asyncio.run(app.shutdown())