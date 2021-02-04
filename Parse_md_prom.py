from typing import Any, Tuple

import requests
import pandas as pd
from bs4 import BeautifulSoup, ResultSet
import pickle
from tqdm import tqdm
import datetime
import time


def get_html(url: str) -> BeautifulSoup:
    try:
        time.sleep(0.5)
        r = requests.get(url)
        return BeautifulSoup(r.text, "html.parser")
    except Exception:

        print(f'Error {url}')


def get_prodpopup(soup: BeautifulSoup) -> ResultSet:
    return soup.findAll('div', attrs={'class': 't754__product-full js-product'})


def get_price(soup: BeautifulSoup) -> str:
    return soup.find('div', attrs={'class': 't754__price-value js-product-price'}).text


def get_title(soup: BeautifulSoup) -> str:
    return soup.find('div', attrs={'class': 't754__title t-name t-name_xl js-product-name'}).text


def get_desc(soup: BeautifulSoup) -> str:
    return soup.find('div', attrs={'class': 't754__descr t-descr t-descr_xxs'}).text


def get_detail_title(soup: BeautifulSoup) -> str:
    return soup.find('h1', attrs={'class': 't760__title t-name t-name_xl js-product-name'}).text


def get_detail_desc(soup: BeautifulSoup) -> str:
    return soup.find('div', attrs={'class': 't760__title_small t-descr t-descr_xxs js-product-sku '}).text


def get_detail_price(soup: BeautifulSoup) -> str:
    try:
        return soup.find('div', attrs={'class': 't760__descr t-descr t-descr_xxs '}).text
    except AttributeError:
        try:
            return soup.find('div', attrs={'class': 't760__price-value js-product-price '}).text
        except AttributeError:
            return '0'


def get_detail_img(soup: BeautifulSoup) -> str:
    return soup.find('img', attrs={'class': 't760__img t-img js-product-img'})['src']


def get_detail_text(soup: BeautifulSoup) -> str:
    return soup.find('div', attrs={'class': 't756__descr t-descr t-descr_xs '})


if __name__ == "__main__":
    # soup = get_html('https://www.md-prom.ru/04md-01')
    # print(get_detail_price(soup))
    date = datetime.date.today()
    data = pd.read_csv('input_file.txt', header=None, names=["Url"])
    data_result = pd.DataFrame(columns=['Url', 'Price', 'Title', 'Desc', 'Text', 'Img'])

    try:
        data_result = pd.read_pickle(f'backup/backup_speed_{date}')
        common = data.merge(data_result, on='Url')
        data = data[~data.Url.isin(common.Url)]
    except FileNotFoundError:
        print('Not found backup')

    with tqdm(total=len(data)) as progress_bar:
        # get prodpopup product
        soup = get_html('https://www.md-prom.ru/product')
        prodpopup = get_prodpopup(soup)
        for soup in prodpopup:
            data_result = data_result.append(
                {'Url': 'Popup', 'Price': get_price(soup), 'Title': get_title(soup), 'Desc': get_desc(soup)},
                ignore_index=True)
        # get product with input file
        for url in data.itertuples():
            try:
                soup = get_html(url.Url)
                price = get_detail_price(soup)
                title = get_detail_title(soup)
                desc = get_detail_desc(soup)
                text = get_detail_text(soup)
                img = get_detail_price(soup)
            except AttributeError:
                price, title, desc, text, img = 0, 0, 0, 0, 0

            data_result = data_result.append(
                {'Url': url.Url, 'Price': price, 'Title': title, 'Desc': desc, 'Text': text, 'Img': img},
                ignore_index=True)
            # data_result.to_pickle(f'backup/backup_speed_{date}')
            progress_bar.update(1)
    data_result.to_csv('result_parse_md-prom.csv', sep=';', encoding='utf-8-sig', index=False)

    print('Nice, maaaaaaan!')
