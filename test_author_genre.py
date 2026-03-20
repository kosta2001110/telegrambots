import requests
from bs4 import BeautifulSoup

URL = 'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
HEADERS = {'User-Agent': 'Mozilla/5.0'}

response = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(response.text, 'lxml')

print("🔍 ТЕСТ АВТОРА И ЖАНРА:")
print("="*60)

# Автор
table = soup.find('table', class_='table table-striped')
if table:
    print("📋 Таблица найдена:")
    for row in table.find_all('tr'):
        th = row.find('th')
        td = row.find('td')
        if th and td:
            print(f"   {th.text.strip()}: {td.text.strip()}")

# Жанр
print("\n🍞 Хлебные крошки:")
breadcrumbs = soup.find('ul', class_='breadcrumb')
if breadcrumbs:
    links = breadcrumbs.find_all('a')
    for i, link in enumerate(links):
        print(f"   [{i}] {link.text.strip()} -> {link['href']}")
    
    if len(links) >= 3:
        print(f"\n📚 Жанр (предпоследний): {links[-2].text.strip()}")
        if len(links) >= 4:
            print(f"📚 Жанр [2]: {links[2].text.strip()}")

print("="*60)