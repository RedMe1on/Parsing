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


def get_specifications(soup: BeautifulSoup) -> pd:
        return soup.find('table', attrs={'class': 'char'}).text


def filter_str(string: str) -> str:
    return string.strip().replace('\n\n', '\n').replace(':\n', ': ').replace('\n\n', '\n')


def _filter_data(data: pd, data_backup: pd) -> pd:
    common = data.merge(data_backup, on='Url')
    return data[~data.Url.isin(common.Url)]


if __name__ == "__main__":
    date = datetime.date.today()
    data = pd.read_csv('input_file.txt', header=None, names=["Url"])
    data_result = pd.DataFrame(columns=['Url', 'Spec'])

    try:
        with open(f'backup/backup_speed_{date}', 'rb') as backup:
            data_result = pickle.load(backup)
            common = data.merge(data_result, on='Url')
            data = data[~data.Url.isin(common.Url)]
    except FileNotFoundError:
        print(FileNotFoundError)

    with tqdm(total=len(data)) as progress_bar:
        for url in data.itertuples():
            try:
                spec = get_specifications(get_html(url.Url))
                spec = filter_str(spec)
            except AttributeError:
                spec = 0
            data_result = data_result.append({'Url': url.Url, 'Spec': spec}, ignore_index=True)
            with open(f'backup/backup_speed_{date}', 'wb') as backup:
                pickle.dump(data_result, backup)
            progress_bar.update(1)
    data_result.to_csv('result_parse_avrora.csv', sep=';', encoding='utf-8-sig', index=False)

    print(data_result)
