import requests
import pandas as pd
from bs4 import BeautifulSoup, ResultSet
import pickle
from tqdm import tqdm
import datetime
import time


def get_res(url: str) -> BeautifulSoup:
    try:
        time.sleep(0.5)
        r = requests.get(url)
        return BeautifulSoup(r.text, "html.parser")
    except Exception:
        print(f'Error {url}')


def get_ru_descr_airlines(soup: BeautifulSoup) -> str:
    return soup.find('p', attrs={'id': 'forum-boxforma'}).text


def get_ru_airlines(soup: BeautifulSoup) -> str:
    return soup.find('p', attrs={'id': 'forum-boxforma'}).find('strong').text


def get_h1_ru_airlines(soup: BeautifulSoup) -> str:
    return soup.find('h1').text


if __name__ == '__main__':
    airlines = []
    airlanes_old = []
    data_result = pd.DataFrame(columns=['old_name', 'url', 'airline', 'descr', 'ru_name'])
    with open('airlines', 'r') as f:
        for line in f:
            airlines.append(str(line.replace(' ', '_').replace('\n', '').lower()))
            airlanes_old.append(str(line))
    print(airlines)
    result = []
    for index, airline in enumerate(airlines):
        url = 'https://www.airlines-inform.ru/world_airlines/' + airline + '.html'
        res = get_res(url)

        try:
            descr = get_ru_descr_airlines(res)
        except:
            descr = None

        try:
            ru_name = get_ru_airlines(res)
        except:
            ru_name = None

        data_result = data_result.append({'old_name': airlanes_old[index], 'url': url, 'airline': airline, 'descr': descr, 'ru_name': ru_name},
                                         ignore_index=True)
    data_result.to_csv('result_airlines.csv')
