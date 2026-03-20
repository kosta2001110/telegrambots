import requests
from bs4 import BeautifulSoup

URL = 'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
HEADERS = {'User-Agent': 'Mozilla/5.0'}

response = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(response.text, 'lxml')

print("📖 ПОИСК ОПИСАНИЯ:")
print("="*60)

# Способ 1: Ищем div с id product_description
desc_div = soup.find('div', id='product_description')
print(f"1. div#product_description: {desc_div is not None}")
if desc_div:
    desc_p = desc_div.find_next_sibling('p')
    if desc_p:
        print(f"   Текст: {desc_p.text[:100]}...")

# Способ 2: Ищем все <p> без class
print("\n2. Все <p> теги:")
all_p = soup.find_all('p')
for i, p in enumerate(all_p[:5]):  # Первые 5
    print(f"   [{i}] class={p.get('class')}, текст: {p.text[:50]}...")

# Способ 3: Ищем после product_description div
print("\n3. Соседи product_description:")
if desc_div:
    for sibling in desc_div.next_siblings:
        if hasattr(sibling, 'name') and sibling.name == 'p':
            print(f"   Нашёл <p>: {sibling.text[:100]}...")
            break

print("="*60)