import time

import requests
from bs4 import BeautifulSoup
import json


def download_categories(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    req = requests.get(url, headers=headers)
    src = req.text

    with open('mains.html', 'w', encoding='utf-8') as file:
        file.write(src)

    with open('mains.html', 'r', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    all_products_hrefs = soup.find_all(class_='checkbox__control')

    all_categories_dict = {}
    delete = ['mm', 'ms', 'ma', 'оa', '', '1_1', 'skidka_p', 'skidka', 'skidka_kat', 'skidki_na_polke',
              'festival_morojenogo', 'bolshe_bonusov', 'haipukii', 'svejee_p']

    for item in all_products_hrefs:
        item_text = item.get('value')
        item_href = 'https://magnit.ru/promo/' + '?' + item.get('name') + '=' + item.get('value')
        # Filter
        if not item_text in delete:
            all_categories_dict[item_text] = item_href

    with open('all_categories_dict.json', 'w', encoding='utf-8') as file:
        json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)


def view_categories():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    with open('all_categories_dict.json') as file:
        all_categories = json.load(file)

    iteration_count = 16
    for category_name, category_href in all_categories.items():
        rep = [',', ' ', '-']
        for item in rep:
            if item in category_name:
                category_name = category_name.replace(item, '_')

        req = requests.get(url=category_href, headers=headers)
        src = req.text

        soup = BeautifulSoup(src, 'lxml')

        product = soup.find_all('a', class_="card-sale_catalogue")

        products_data_list = []

        for item in product:
            try:
                name = item.find(class_='card-sale__col_content').find(class_='card-sale__title').find('p').text
            except Exception:
                name = 'Нет названия продукта'
            try:
                new_price_integer = item.find(class_='label__price_new').find(class_='label__price-integer').text
                new_price_decimal = item.find(class_='label__price_new').find(class_='label__price-decimal').text
                final_new_price = str(new_price_integer) + '.' + str(new_price_decimal)
            except Exception:
                final_new_price = 'Нет цены'
            try:
                start_date = soup.find(class_='card-sale__date').find('p').text
                end_date = soup.find(class_='card-sale__date').find_all('p')
                end_date = end_date[1].text
            except Exception:
                start_date = 'Нет начала'
                end_date = 'Нет конца'
            try:
                old_price_integer = item.find(class_='label__price_old').find(class_='label__price-integer').text
                old_price_decimal = item.find(class_='label__price_old').find(class_='label__price-decimal').text
                final_old_price = str(old_price_integer) + '.' + str(old_price_decimal)
            except Exception:
                final_old_price = 'Нет цены'

            if final_old_price != 'Нет цены' and final_new_price != 'Нет цены' and name != 'Нет названия продукта' \
                    and name is not None:
                discount = round(((float(final_old_price) - float(final_new_price)) / float(final_old_price)) * 100)
                products_data_list.append({
                    'Название товара': name,
                    'Старая цена товара': final_old_price,
                    'Новая цена товара': final_new_price,
                    'Процент скидки': str(discount),
                    'Длительность акции': {'Начало акции': start_date, 'Конец акции': end_date}
                })
            if not products_data_list:
                continue
            else:
                with open(f'data/{category_name}_products_data_list.json', 'w', encoding='utf-8') as file:
                    json.dump(products_data_list, file, indent=4, ensure_ascii=False)


def main():
    # download_categories('https://magnit.ru/promo/')
    view_categories()


if __name__ == '__main__':
    main()
