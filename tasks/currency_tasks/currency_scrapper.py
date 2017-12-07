import os
import requests

from bs4 import BeautifulSoup
from pathlib import Path


class CurrencyParser:

    FILE = 'currency.txt'
    URL = 'https://goo.gl/b4oeUz'

    def __init__(self):
        self.html = requests.get(self.URL).text
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.table = self.soup.find(class_='wikitable')

    def collect_data(self):
        data = list()
        trs = self.table.find_all('tr')
        for tr in trs:
            rows = tr.find_all('td')
            row = [column.text.strip() for i, column in enumerate(rows) if i in (0, 1, 5, 6)]
            if len(row) == 4:
                data.append(row)
        return data

    @staticmethod
    def clear_data(data):
        for item in data:
            item[0] = item[0].split(u'\xa0')[0]
            item[1] = item[1].replace('\n', ' ')
            item[2] = item[2].replace('\n', ' ')
        return data

    def write_data(self, data):
        if Path(self.FILE).exists():
            os.remove(self.FILE)
        with open(self.FILE, 'a') as f:
            for item in data:
                f.write(', '.join(item) + '\n')


if __name__ == "__main__":
    cp = CurrencyParser()
    data = cp.collect_data()
    cp.write_data(cp.clear_data(data))
