import requests
import pandas as pd
from bs4 import BeautifulSoup
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


def get_specifications(soup: BeautifulSoup) -> str:
    return soup.find('table', attrs={'class': 'char'}).text


def get_major_image_url(soup: BeautifulSoup) -> str:
    soup = soup.find('div', attrs={'class': 'gallery-item__content'})
    return soup.img['src']


def filter_str(string: str) -> str:
    return string.strip().replace('\n\n', '\n').replace(':\n', ': ').replace('\n\n', '\n')


if __name__ == "__main__":

    date = datetime.date.today()
    data = pd.read_csv('input_file.txt', header=None, names=["Url"])
    data_result = pd.DataFrame(columns=['Url', 'Spec', 'Major_image'])

    try:
        data_result = pd.read_pickle(f'backup/backup_speed_{date}')
        common = data.merge(data_result, on='Url')
        data = data[~data.Url.isin(common.Url)]
    except FileNotFoundError:
        print('Not found backup')

    with tqdm(total=len(data)) as progress_bar:
        for url in data.itertuples():
            try:
                soup = get_html(url.Url)
                spec = get_specifications(soup)
                spec = filter_str(spec)
            except AttributeError:
                spec = 0
            try:
                image_url = get_major_image_url(soup)
            except AttributeError:
                image_url = 0


            data_result = data_result.append({'Url': url.Url, 'Spec': spec, 'Major_image': image_url},
                                             ignore_index=True)
            data_result.to_pickle(f'backup/backup_speed_{date}')
            progress_bar.update(1)
    data_result.to_csv('result_parse_avrora.csv', sep=';', encoding='utf-8-sig', index=False)

    print('Nice, maaaaaaan!')
