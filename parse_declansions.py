import urllib
from urllib.parse import quote

import requests
import pandas as pd
from bs4 import BeautifulSoup, ResultSet
import pickle
from tqdm import tqdm
import datetime
import time

URL = 'https://www.translate.ru/%D1%81%D0%BF%D1%80%D1%8F%D0%B6%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%B8%20%D1%81%D0%BA%D0%BB%D0%BE%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5/%D1%80%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9/'


def get_res(url: str, word: str) -> BeautifulSoup:
    try:
        word = quote(word)
        time.sleep(1)
        r = requests.get(url + word)
        return BeautifulSoup(r.text, "html.parser")
    except Exception:
        print(f'Error {url}')


def get_declansion_table(soup: BeautifulSoup):
    return soup.find('div', attrs={'class': 'wordforms table'})


def get_rows(soup: BeautifulSoup):
    return soup.findAll('div', attrs={'class': 'tr desk'})


def get_cases(soup: BeautifulSoup):
    return soup.findAll('div', attrs={'class': 'td'})


def main():
    result = {}
    countries = []
    cases_arr = ['Именительный падеж  (Кто? Что?)',
                 'Родительный падеж (Кого? Чего?)',
                 'Дательный падеж (Кому? Чему?)',
                 'Винительный падеж (Кого? Что?)',
                 'Творительный падеж (Кем? Чем?)',
                 'Предложный падеж (О ком? О чем?)'
                 ]
    with open('countries', 'r', encoding="utf8") as file:
        for line in file:
            countries.append(line.strip().strip('\r\n\t'))
    with tqdm(total=len(countries)) as progress_bar:
        for country in countries:
            result[country] = {}
            try:
                res = get_res(URL, country)

                table = get_declansion_table(res)
                rows = get_rows(table)
            except:
                rows = []
                for case in cases_arr:
                    result[country][case] = {
                        'solo': '-',
                        'multi': '-'
                    }
            for row in rows:
                cases = get_cases(row)

                result[country][cases[0].text.strip('\r\n\t').strip()] = {
                    'solo': cases[1].text.strip('\r\n\t').strip(),
                    'multi': cases[2].text.strip('\r\n\t').strip()
                }

                # print(row)
                # for case in cases:
                #
                #     print(case.text)

            with open('result_declansions.csv', 'w', encoding='utf8') as f:
                header = ','.join([case for case in result[countries[0]].keys()])
                f.write(f'Страна, {header}\n')
                for country in result:
                    solo = ','.join([result[country][case]['solo'] for case in cases_arr])
                    multi = ','.join([result[country][case]['multi'] for case in cases_arr])
                    f.write(f'{country},{solo}\n')
                    f.write(f'{country}_multi,{multi}\n')

            progress_bar.update(1)


if __name__ == '__main__':
    main()
