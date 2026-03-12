import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime

# ============================================
# === НАСТРОЙКИ ===
# ============================================

BASE_URL = 'https://books.toscrape.com/'
TOTAL_PAGES = 10  # 10 страниц × 20 книг = 200 книг
HEADERS = {'User-Agent': 'Mozilla/5.0'}

# ============================================
# === ПАРСИНГ ВСЕХ СТРАНИЦ ===
# ============================================

def parse_all_books():
    all_books = []
    
    print("🔌 Запуск парсера (200 книг)...")
    print(f"📅 Дата: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"📚 Страниц: {TOTAL_PAGES}")
    print("="*50)
    
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
                
                data = {
                    'title': title,
                    'price': price,
                    'rating': rating,
                    'link': link,
                    'page': page,
                    'parsed_date': datetime.now().strftime('%Y-%m-%d %H:%M')
                }
                all_books.append(data)
                
            except Exception as e:
                print(f"   ❌ Ошибка книги: {e}")
                continue
        
        # Задержка чтобы не блокировали
        time.sleep(1)
    
    # ============================================
    # === СОХРАНЕНИЕ ===
    # ============================================
    
    if all_books:
        df = pd.DataFrame(all_books)
        df.to_csv('books_day2_200.csv', index=False, encoding='utf-8-sig')
        df.to_excel('books_day2_200.xlsx', index=False)
        
        print(f"\n{'='*50}")
        print(f"✅ ВСЕГО: {len(all_books)} книг")
        print(f"📁 Файлы: books_day2_200.csv, books_day2_200.xlsx")
        
        # Статистика
        print(f"\n📊 СТАТИСТИКА:")
        print(f"   Уникальных рейтингов: {df['rating'].nunique()}")
        print(f"   Диапазон цен: {df['price'].min()} - {df['price'].max()}")
        print(f"{'='*50}")
    else:
        print("\n⚠️ Нет данных")

    return all_books

if __name__ == '__main__':
    parse_all_books()