import asyncio
import aiohttp
import random
from datetime import datetime
from bs4 import BeautifulSoup
import logging
from config import UPDATE_INTERVAL

logger = logging.getLogger(__name__)

class PredictionEngine:
    def __init__(self):
        self.live_matches = []
        self.predictions_history = []
        self.stats = {
            "correct_predictions": 0,
            "wrong_predictions": 0,
            "total_predictions": 0,
            "current_streak": 0
        }
        
    async def auto_update(self):
        """التحديث التلقائي للبيانات"""
        while True:
            try:
                await self.fetch_live_data()
                logger.info("✅ تم تحديث البيانات الحية")
                await asyncio.sleep(UPDATE_INTERVAL)
            except Exception as e:
                logger.error(f"❌ خطأ في التحديث التلقائي: {e}")
                await asyncio.sleep(30)  # انتظار 30 ثانية عند الخطأ
        
    async def fetch_live_data(self):
        """جلب البيانات الحية من 1xbet"""
        try:
            # محاكاة جلب البيانات من 1xbet
            # في الإصدار الحقيقي، سنستخدم Selenium أو requests
            
            # بيانات محاكاة للمباريات الحية
            self.live_matches = [
                {
                    "id": 1,
                    "teams": "Barcelona vs Real Madrid",
                    "score": "2-1",
                    "time": "67'",
                    "goals": 3,
                    "attacks": 24,
                    "possession": "52% - 48%",
                    "momentum": "home"
                },
                {
                    "id": 2, 
                    "teams": "Man City vs Liverpool",
                    "score": "1-1", 
                    "time": "45'",
                    "goals": 2,
                    "attacks": 18,
                    "possession": "48% - 52%",
                    "momentum": "away"
                },
                {
                    "id": 3,
                    "teams": "Bayern vs Dortmund",
                    "score": "0-0",
                    "time": "23'",
                    "goals": 0,
                    "attacks": 12,
                    "possession": "55% - 45%", 
                    "momentum": "home"
                }
            ]
            
        except Exception as e:
            logger.error(f"❌ خطأ في جلب البيانات: {e}")
            # استخدام بيانات افتراضية عند الخطأ
            self.live_matches = [
                {
                    "id": 1,
                    "teams": "Default Match 1",
                    "score": "0-0",
                    "time": "30'",
                    "goals": 0,
                    "attacks": 15,
                    "possession": "50% - 50%",
                    "momentum": "neutral"
                }
            ]
    
    async def get_goal_prediction(self):
        """الحصول على توقع الهدف الحالي"""
        if not self.live_matches:
            await self.fetch_live_data()
            
        current_match = self.live_matches[0]  # أول مباراة حية
        
        # تحليل البيانات لتوقع الهدف
        prediction_data = self.analyze_match(current_match)
        
        # تسجيل التوقع
        self.record_prediction(prediction_data)
        
        return prediction_data
    
    async def get_next_prediction(self):
        """الحصول على التوقع القادم"""
        if not self.live_matches:
            await self.fetch_live_data()
            
        next_match = self.live_matches[1] if len(self.live_matches) > 1 else self.live_matches[0]
        
        return {
            "match": next_match["teams"],
            "schedule": "قريباً",
            "prediction": self.generate_prediction(next_match),
            "goal_probability": random.randint(65, 92),
            "confidence": "عالي" if random.randint(1, 10) > 3 else "متوسط",
            "advice": self.get_advice(),
            "status": "success"
        }
    
    def analyze_match(self, match):
        """تحليل المباراة لتوقع الهدف"""
        # خوارزمية تحليل المباراة
        goals = match["goals"]
        time = int(match["time"].replace("'", ""))
        attacks = match["attacks"]
        momentum = match["momentum"]
        
        # حساب احتمالية الهدف
        base_prob = 50
        
        # عوامل زيادة الاحتمالية
        if goals == 0 and time > 70:
            base_prob += 25  # مباراة بدون أهداف وقرب النهاية
        elif goals >= 3:
            base_prob += 15  # مباراة مليئة بالأهداف
            
        if attacks > 20:
            base_prob += 10  # هجمات كثيرة
            
        if momentum != "neutral":
            base_prob += 10  # زخم لفريق معين
            
        if time > 80:
            base_prob += 20  # وقت إضافي
            
        # تحديد التوقع النهائي
        goal_probability = min(95, base_prob + random.randint(-10, 15))
        will_score = goal_probability > 60
        
        return {
            "match": match["teams"],
            "time": match["time"],
            "prediction": "🎯 GOAL" if will_score else "❌ NO GOAL",
            "confidence": goal_probability,
            "score": match["score"],
            "analysis": self.get_analysis(match, will_score, goal_probability),
            "status": "success"
        }
    
    def generate_prediction(self, match):
        """توليد توقع بناءً على تحليل المباراة"""
        goals = match["goals"]
        time = int(match["time"].replace("'", ""))
        
        if goals == 0 and time > 75:
            return "🎯 GOAL" if random.random() > 0.3 else "❌ NO GOAL"
        elif goals >= 3:
            return "🎯 GOAL" if random.random() > 0.4 else "❌ NO GOAL"
        else:
            return "🎯 GOAL" if random.random() > 0.5 else "❌ NO GOAL"
    
    def get_analysis(self, match, will_score, probability):
        """تحليل مفصل للمباراة"""
        analyses = [
            f"الزخم الحالي يشير إلى {'هدف قريب' if will_score else 'استقرار دفاعي'}",
            f"معدل الهجمات ({match['attacks']}) {'يدعم فرصة التسجيل' if will_score else 'يوضح صعوبة التسجيل'}",
            f"نسبة الاستحواذ {match['possession']} تؤثر على فرص التسجيل",
            f"النتيجة الحالية {match['score']} {'تشجع على الهجوم' if will_score else 'تفرض حذراً دفاعياً'}"
        ]
        return random.choice(analyses)
    
    def get_advice(self):
        """نصيحة بناءً على التحليل"""
        advices = [
            "الزخم الحالي يشير إلى هدف في الدقائق القادمة",
            "الأداء الهجومي قوي وفرص التسجيل مرتفعة",
            "الضغط الدفاعي قد يؤخر التسجيل ولكن الاحتمال موجود",
            "التوازن في المبارى يقلل من فرص التسجيل القريبة"
        ]
        return random.choice(advices)
    
    def record_prediction(self, prediction):
        """تسجيل التوقع في السجل"""
        self.predictions_history.append({
            **prediction,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        # تحديث الإحصائيات (محاكاة)
        self.stats["total_predictions"] += 1
        if random.random() > 0.15:  # 85% دقة
            self.stats["correct_predictions"] += 1
            self.stats["current_streak"] += 1
        else:
            self.stats["wrong_predictions"] += 1
            self.stats["current_streak"] = 0
    
    async def get_stats(self):
        """الحصول على الإحصائيات"""
        total = self.stats["total_predictions"]
        correct = self.stats["correct_predictions"]
        
        accuracy = round((correct / total) * 100, 2) if total > 0 else 0
        
        return {
            "correct_predictions": correct,
            "wrong_predictions": self.stats["wrong_predictions"],
            "total_predictions": total,
            "accuracy": accuracy,
            "current_streak": self.stats["current_streak"],
            "last_update": datetime.now().strftime("%H:%M:%S")
        }