#!/usr/bin/env python3
import telebot
import sqlite3
import logging
import os

# Настройки
BOT_TOKEN = os.getenv('BOT_TOKEN', 'ТВОЙ_ТОКЕН_ЗДЕСЬ')
DB_NAME = 'books_database_v2.db'

bot = telebot.TeleBot(BOT_TOKEN)

# Логирование
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# Команда /start
@bot.message_handler(commands=['start'])
def start_cmd(message):
    logger.info(f"/start от {message.from_user.username}")
    bot.reply_to(message, "👋 Привет! Я Book Bot.\n\n📚 Парсю книги, анализирую цены.\n\nКоманды:\n/books — показать книги\n/stats — статистика")

# Команда /books
@bot.message_handler(commands=['books'])
def books_cmd(message):
    logger.info(f"/books от {message.from_user.username}")
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT title, price, rating FROM books LIMIT 5')
        books = cursor.fetchall()
        conn.close()
        
        response = "📚 Последние книги:\n\n"
        for title, price, rating in books:
            response += f"• {title[:30]}... — {price} ⭐{rating}\n"
        bot.reply_to(message, response)
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

# Команда /stats
@bot.message_handler(commands=['stats'])
def stats_cmd(message):
    logger.info(f"/stats от {message.from_user.username}")
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*), AVG(CAST(REPLACE(price, "Â£", "") AS REAL)) FROM books')
        count, avg_price = cursor.fetchone()
        conn.close()
        bot.reply_to(message, f"📊 Статистика:\n\n📚 Всего книг: {count}\n💰 Средняя цена: £{avg_price:.2f}")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

# Обработка всех сообщений
@bot.message_handler(func=lambda message: True)
def all_messages(message):
    logger.info(f"💬 {message.from_user.username}: {message.text}")
    bot.reply_to(message, "🤖 Не понял команду. Напиши /start для помощи.")

# Запуск
if __name__ == '__main__':
    logger.info("🚀 Book Bot запущен!")
    bot.infinity_polling(timeout=30)