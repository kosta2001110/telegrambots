# 📚 Telegram Parser + ML

Парсер книг с books.toscrape.com + ML анализ + Telegram-бот

## 🚀 Возможности

- ✅ Парсинг многостраничного каталога
- ✅ Сохранение в SQLite базу данных
- ✅ Telegram-бот с уведомлениями
- ✅ ML анализ цен (линейная регрессия)

## 📁 Файлы

- `day1_parser.py` — простой парсер (20 книг)
- `day2_parser.py` — парсер 200 книг
- `day3_database.py` — парсер с SQLite
- `day3_bot.py` — Telegram-бот
- `day2_analysis.ipynb` — анализ данных
- `day3_ml.ipynb` — ML модели

## 🛠 Установка

```bash
pip install requests beautifulsoup4 pandas sqlite3 pyTelegramBotAPI scikit-learn