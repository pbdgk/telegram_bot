#  todo fix xTimes importing same module
import requests
import pickle
from pathlib import Path
from bs4 import BeautifulSoup

import os.path

dir_path = os.path.dirname(os.path.realpath(__file__))


class CurrencyScrapper:

    FILE = os.path.join(dir_path, 'currency.pickle')
    URL = 'https://goo.gl/iFHWsJ'

    def __init__(self):
        self.html = requests.get(self.URL).text
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.table = self.soup.find('table')

    def _collect_data(self):
        data_ = list()
        trs = self.table('tr')
        for tr in trs:
            data_.append([el.text for el in tr])
        return data_

    def _get_values(self):
        d = dict()
        data_ = self._collect_data()
        e_countries = set()
        for el in data_[1:]:
            if not el[0] == 'EUR':
                d.update({el[0]: ', '.join(el)})
            else:
                e_countries.add(el[2])
        e_countries = ', '.join(e_countries)
        d.update({'EUR': ', '.join(('EUR', 'Euro', 'Europe', e_countries))})
        return d

    def read_data(self):
        with open(self.FILE, 'rb') as f:
            return pickle.load(f)

    def write_data(self, data_):
        with open(self.FILE, 'wb') as f:
                pickle.dump(data_, f)

    def get_currencies(self):
        path = Path(self.FILE)
        if path.exists():
            return self.read_data()
        else:
            values = self._get_values()
            self.write_data(values)
            return values


if __name__ == "__main__":
    cp = CurrencyScrapper()
    data = cp.get_currencies()
    from pprint import pprint
    pprint(data)

