import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import time
import logging
import json

# ============================================
# === НАСТРОЙКИ ===
# ============================================

BASE_URL = 'https://books.toscrape.com/'
TOTAL_PAGES = 5
HEADERS = {'User-Agent': 'Mozilla/5.0'}
DB_NAME = 'books_database_v2.db'

# ============================================
# === ЛОГИРОВАНИЕ ===
# ============================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('day5_parser_log.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# ============================================
# === СОЗДАНИЕ БАЗЫ ДАННЫХ (НОВАЯ СТРУКТУРА) ===
# ============================================

def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT,
            genre TEXT,
            price TEXT NOT NULL,
            rating TEXT NOT NULL,
            availability TEXT,
            description TEXT,
            link TEXT NOT NULL,
            page INTEGER,
            parsed_date TEXT NOT NULL,
            UNIQUE(title, page)
        )
    ''')
    
    conn.commit()
    conn.close()
    logger.info("✅ База данных v2 создана!")

# ============================================
# === ПАРСИНГ ДЕТАЛЬНОЙ СТРАНИЦЫ КНИГИ ===
# ============================================

def parse_book_details(book_link):
    """Парсинг дополнительной информации со страницы книги"""
    try:
        response = requests.get(book_link, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            return None, None, None
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        # === АВТОР (может отсутствовать!) ===
        author = None
        table = soup.find('table', class_='table table-striped')
        if table:
            for row in table.find_all('tr'):
                th = row.find('th')
                td = row.find('td')
                if th and td and 'Author' in th.text:
                    author = td.text.strip()
                    break
            # Если не нашли, оставляем None (нормально!)
        
        # === ЖАНР (3-й элемент, индекс 2) ===
        genre = None
        breadcrumbs = soup.find('ul', class_='breadcrumb')
        if breadcrumbs:
            links = breadcrumbs.find_all('a')
            # Структура: Home [0] > Books [1] > Genre [2]
            if len(links) >= 3:
                genre = links[2].text.strip()  # Индекс 2, не -2!
        
        # === ОПИСАНИЕ ===
        description = None
        desc_div = soup.find('div', id='product_description')
        if desc_div:
            desc_p = desc_div.find_next_sibling('p')
            if desc_p:
                description = desc_p.text.strip()[:200]
        
        return author, genre, description
    
    except Exception as e:
        logger.warning(f"⚠️ Ошибка парсинга деталей: {e}")
        return None, None, None
    
# ============================================
# === ОСНОВНОЙ ПАРСИНГ ===
# ============================================

def parse_and_save():
    create_database()
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    logger.info("🔌 Запуск улучшенного парсера...")
    logger.info(f"📅 Дата: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    logger.info("="*60)
    
    total_books = 0
    detailed_books = 0
    
    for page in range(1, TOTAL_PAGES + 1):
        url = f'{BASE_URL}catalogue/page-{page}.html'
        logger.info(f"\n📖 Страница {page}...")
        
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code != 200:
            logger.error(f"   ❌ Ошибка: {response.status_code}")
            break
        
        soup = BeautifulSoup(response.text, 'lxml')
        books = soup.find_all('article', class_='product_pod')
        
        logger.info(f"   Найдено книг: {len(books)}")
        
        for i, book in enumerate(books):
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
                    # Парсим детали (каждую 3-ю книгу для скорости)
                    author, genre, description = None, None, None
                    if i % 3 == 0:  # Каждая 3-я книга для демо
                        logger.info(f"   📖 Детали: {title[:30]}...")
                        author, genre, description = parse_book_details(link)
                        detailed_books += 1
                        time.sleep(1)  # Задержка чтобы не блокировали
                    
                    # Доступность
                    availability = book.find('p', class_='instock availability')
                    availability = availability.text.strip() if availability else 'Unknown'
                    
                    cursor.execute('''
                        INSERT INTO books (title, author, genre, price, rating, 
                                         availability, description, link, page, parsed_date)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (title, author, genre, price, rating, 
                          availability, description, link, page, parsed_date))
                    
                    total_books += 1
                    logger.info(f"   ✓ {title[:40]}... | {genre or 'N/A'}")
                
            except Exception as e:
                logger.error(f"   ❌ Ошибка: {e}")
                continue
        
        time.sleep(1)
    
    conn.commit()
    conn.close()
    
    logger.info(f"\n{'='*60}")
    logger.info(f"✅ СОХРАНЕНО: {total_books} книг")
    logger.info(f"📊 С деталями: {detailed_books} книг")
    logger.info(f"📁 База данных: {DB_NAME}")
    logger.info(f"{'='*60}")

# ============================================
# === ВАЛИДАЦИЯ ДАННЫХ ===
# ============================================

def validate_data():
    """Проверка качества данных"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    logger.info("\n🔍 ВАЛИДАЦИЯ ДАННЫХ:")
    logger.info("="*60)
    
    # Всего книг
    cursor.execute('SELECT COUNT(*) FROM books')
    total = cursor.fetchone()[0]
    logger.info(f"📚 Всего книг: {total}")
    
    # Пропуски в полях
    fields = ['author', 'genre', 'availability', 'description']
    for field in fields:
        cursor.execute(f'SELECT COUNT(*) FROM books WHERE {field} IS NULL')
        null_count = cursor.fetchone()[0]
        percentage = (null_count / total * 100) if total > 0 else 0
        logger.info(f"   {field}: {null_count} пропусков ({percentage:.1f}%)")
    
    # Дубликаты
    cursor.execute('''
        SELECT title, COUNT(*) as cnt 
        FROM books 
        GROUP BY title 
        HAVING cnt > 1
    ''')
    duplicates = cursor.fetchall()
    if duplicates:
        logger.warning(f"⚠️ Найдено дубликатов: {len(duplicates)}")
    else:
        logger.info("✅ Дубликатов нет")
    
    # Статистика по жанрам
    cursor.execute('SELECT genre, COUNT(*) FROM books WHERE genre IS NOT NULL GROUP BY genre')
    genres = cursor.fetchall()
    logger.info(f"\n📚 Жанры ({len(genres)} уникальных):")
    for genre, count in sorted(genres, key=lambda x: x[1], reverse=True)[:10]:
        logger.info(f"   {genre}: {count} книг")
    
    conn.close()
    logger.info("="*60)

# ============================================
# === ЗАПУСК ===
# ============================================

if __name__ == '__main__':
    parse_and_save()
    validate_data()