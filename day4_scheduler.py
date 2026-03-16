import schedule
import time
from datetime import datetime
import logging
from day3_database import parse_and_save

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('parser_log.log', encoding='utf-8'),
    ]
)

logger = logging.getLogger(__name__)

# ============================================
# === ФУНКЦИЯ ЗАДАЧИ ===
# ============================================

def job():
    """Задача, которая будет выполняться по расписанию"""
    logger.info("🔄 Запуск парсера по расписанию...")
    
    try:
        parse_and_save()  # Вызываем функцию из day3_database.py
        logger.info("✅ Парсинг завершён успешно!")
    except Exception as e:
        logger.error(f"❌ Ошибка при парсинге: {e}")

# ============================================
# === РАСПИСАНИЕ ===
# ============================================

def setup_schedule():
    """Настраиваем расписание"""
    
    # Варианты (раскомментируй нужный):
    
    # ✅ Каждый день в 9:00 утра
    schedule.every().day.at("09:00").do(job)
    
    # ✅ Каждые 6 часов
    # schedule.every(6).hours.do(job)
    
    # ✅ Каждый понедельник в 10:00
    # schedule.every().monday.at("10:00").do(job)
    
    # ✅ Для теста: каждые 10 минут
    # schedule.every(10).minutes.do(job)
    
    logger.info("📅 Расписание настроено!")

# ============================================
# === ЗАПУСК ===
# ============================================

if __name__ == '__main__':
    logger.info("🚀 Scheduler запущен!")
    logger.info(f"📅 Дата: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*60)
    
    setup_schedule()
    
    # Главный цикл
    while True:
        schedule.run_pending()
        time.sleep(60)  # Проверяем каждую минуту