import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import time

# ============================================
# === НАСТРОЙКИ ===
# ============================================

BASE_URL = 'https://books.toscrape.com/'
TOTAL_PAGES = 5  # Для теста 5 страниц
HEADERS = {'User-Agent': 'Mozilla/5.0'}
DB_NAME = 'books_database.db'

# ============================================
# === СОЗДАНИЕ БАЗЫ ДАННЫХ ===
# ============================================

def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            price TEXT NOT NULL,
            rating TEXT NOT NULL,
            link TEXT NOT NULL,
            page INTEGER,
            parsed_date TEXT NOT NULL,
            UNIQUE(title, page)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ База данных создана!")

# ============================================
# === ПАРСИНГ + СОХРАНЕНИЕ В БД ===
# ============================================

def parse_and_save():
    create_database()
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    print("🔌 Запуск парсера с сохранением в БД...")
    print(f"📅 Дата: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*50)
    
    total_books = 0
    
    for page in range(1, TOTAL_PAGES + 1):
        url = f'{BASE_URL}catalogue/page-{page}.html'
        print(f"\n📖 Страница {page}...")
        
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code != 200:
            print(f"   ❌ Ошибка: {response.status_code}")
            break
        
        soup = BeautifulSoup(response.text, 'lxml')
        books = soup.find_all('article', class_='product_pod')
        
        print(f"   Найдено книг: {len(books)}")
        
        for book in books:
            try:
                title = book.find('h3').find('a')['title']
                price = book.find('p', class_='price_color').text
                rating_class = book.find('p', class_='star-rating')['class']
                rating = rating_class[1] if len(rating_class) > 1 else 'No Rating'
                link = BASE_URL + 'catalogue/' + book.find('h3').find('a')['href']
                parsed_date = datetime.now().strftime('%Y-%m-%d %H:%M')
                
                # Проверка на дубликаты
                cursor.execute('SELECT id FROM books WHERE title = ? AND page = ?', (title, page))
                if cursor.fetchone() is None:
                    cursor.execute('''
                        INSERT INTO books (title, price, rating, link, page, parsed_date)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (title, price, rating, link, page, parsed_date))
                    total_books += 1
                    print(f"   ✓ {title[:40]}...")
                
            except Exception as e:
                print(f"   ❌ Ошибка: {e}")
                continue
        
        time.sleep(1)
    
    conn.commit()
    conn.close()
    
    print(f"\n{'='*50}")
    print(f"✅ СОХРАНЕНО: {total_books} новых книг")
    print(f"📁 База данных: {DB_NAME}")
    print(f"{'='*50}")
    
    # Статистика из БД
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM books')
    total = cursor.fetchone()[0]
    print(f"📊 ВСЕГО в базе: {total} книг")
    conn.close()

# ============================================
# === ЗАПУСК ===
# ============================================

if __name__ == '__main__':
    parse_and_save()