from lxml import html
import requests
import re


def clean_price(price_text) -> float:
    '''
    Функция, преобразующая строковое представление стоимости в числовое
    :param price_text: str
    :return: float
    '''
    cleaned = re.sub(r'[^\d.]', '', price_text)
    return float(cleaned) if cleaned else 0.0


def parse_prices_for_site(url, xpath):
    prices = []
    try:
        response = requests.get(url)
        tree = html.fromstring(response.content)
        price_elements = tree.xpath(xpath)

        # Собираем цены всех товаров
        for element in price_elements:
            price_text = element.text_content().strip()
            price = clean_price(price_text)
            prices.append(price)
        print(prices)  # оставил для наглядности

        # Вычисляем среднюю цену
        if prices:
            average_price = round(sum(prices) / len(prices), 2)
            return average_price
        else:
            return None
    except Exception as e:
        print(f'Ошибка при парсинге {url}: {e}')
        return None


def parse_prices(df):
    results = {}
    for index, row in df.iterrows():
        title = row['title']
        url = row['url']
        xpath = row['xpath']

        average_price = parse_prices_for_site(url, xpath)

        if average_price is not None:
            results[title] = average_price
        else:
            results[title] = 'Цены не найдены'
    return results
