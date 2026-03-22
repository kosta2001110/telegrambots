#!/usr/bin/env python3
import telebot
import logging
import os
from day3_bot import handle_message, send_welcome  # Импорт из твоего бота

# Настройки
BOT_TOKEN = os.getenv('BOT_TOKEN', 'ТВОЙ_ТОКЕН_ЗДЕСЬ')
bot = telebot.TeleBot(BOT_TOKEN)

# Логирование
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot_log.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

@bot.message_handler(commands=['start'])
def start_cmd(message):
    send_welcome(message)

@bot.message_handler(func=lambda message: True)
def all_messages(message):
    handle_message(message)

if __name__ == '__main__':
    logger.info("🚀 Бот запущен на сервере!")
    bot.infinity_polling(timeout=30, long_polling_timeout=30)