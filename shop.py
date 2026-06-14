import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import json
def page_parser(url):
    all_card = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f'Ошибка запроса: {e}')
        return [], None
    soup = BeautifulSoup(response.text, 'html.parser')
    names = soup.find_all('li', class_='product')
    for title in names:
        name_card = title.find('a')
        name = name_card.find('h2').text
        price_text = name_card.find('span').text.strip().replace('$', '')
        price = float(price_text)
        link = name_card['href']
        image = name_card.find('img')['src']
        all_card.append({'name': name, 'price': price, 'link': link, 'image': image})
    return all_card, soup
def next_page_url(url, soup):
    next_button = soup.find('a', class_='next page-numbers')
    if next_button:
        return urljoin(url, next_button['href'])
    return None
def sorted_card(all_card):
    return sorted(all_card, key=lambda item: item['price'], reverse=True)
def save_to_csv(all_card):
    with open('shop.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'price', 'link', 'image'])
        for item in all_card:
            writer.writerow([item['name'], item['price'], item['link'], item['image']])
def save_to_json(all_card):
    with open('shop.json', 'w', encoding='utf-8') as file:
        json.dump(all_card, file, ensure_ascii=False, indent=4)
def main():
    url_base = 'https://www.scrapingcourse.com/ecommerce/'
    url = url_base
    all_card_global = []
    page = 1
    limit = 5
    while url and page <= limit:
        all_card, soup = page_parser(url)
        if soup is None:
            break
        all_card_global.extend(all_card)
        url = next_page_url(url, soup)
        page += 1
    sort_card = sorted_card(all_card_global)
    save_to_csv(sort_card)
    save_to_json(sort_card)
    print(f'Готово! Собрано товаров: {len(sort_card)}')
if __name__ == "__main__":
    main()