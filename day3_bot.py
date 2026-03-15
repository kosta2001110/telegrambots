import requests
from bs4 import BeautifulSoup
import sqlite3
import telebot
from datetime import datetime
import time

# ============================================
# === НАСТРОЙКИ ===
# ============================================

BOT_TOKEN = '8617561077:AAGZoWVkjtjtWQQJ4_B6Qzn03vx7FecD3po'  # ← ВСТАВЬ СВОЙ ТОКЕН!
CHAT_ID = '7779368218'  # ← ВСТАВЬ СВОЙ CHAT ID!
BASE_URL = 'https://books.toscrape.com/'
HEADERS = {'User-Agent': 'Mozilla/5.0'}
DB_NAME = 'books_database.db'

print("🤖 Запуск бота...")
print(f"📋 Token: {BOT_TOKEN[:25]}...")
print(f"📋 Chat ID: {CHAT_ID}")

# ============================================
# === ИНИЦИАЛИЗАЦИЯ БОТА ===
# ============================================

try:
    bot = telebot.TeleBot(BOT_TOKEN)
    print("✅ Бот инициализирован!")
except Exception as e:
    print(f"❌ Ошибка: {e}")
    exit()

# ============================================
# === ПРОВЕРКА БАЗЫ ===
# ============================================

print("🔍 Проверка базы данных...")

try:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM books')
    total = cursor.fetchone()[0]
    print(f"📚 В базе: {total} книг")
    
    conn.close()
except Exception as e:
    print(f"❌ Ошибка БД: {e}")
    exit()

# ============================================
# === ТЕСТОВОЕ СООБЩЕНИЕ ===
# ============================================

print("📤 Отправка тестового сообщения...")

try:
    message = f"🤖 **БОТ ЗАПУЩЕН!**\n\n📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n✅ Бот работает!\n📚 Книг в базе: {total}"
    bot.send_message(CHAT_ID, message, parse_mode='Markdown')
    print("✅ СООБЩЕНИЕ ОТПРАВЛЕНО!")
except Exception as e:
    print(f"❌ Ошибка отправки: {e}")
    print("💡 Проверь токен и Chat ID!")

print("="*50)