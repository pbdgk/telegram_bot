import requests
from tasks.currency_tasks.currency_scrapper import CurrencyScrapper


class Currency:
    def __init__(self):
        self.currencies = CurrencyScrapper().get_currencies()

    async def do_task(self, vars_, new_message):
        if not new_message and not vars_:
            return 'Enter base currency', None
        elif new_message and not vars_:
            return 'Is it your base currency?', self.is_currency_real(new_message)
        elif new_message and vars_:
            return 'Is it your next currency?', self.is_currency_real(new_message)

    def is_currency_real(self, key) -> list:
        currency = self.currencies.get(key.upper())
        if currency:
            l = list()
            l.append(key)
            return l
        currencies = []
        for k in self.currencies:
            if k.startswith(key.upper()):
                currencies.append(k)
        return currencies[:4]

    @staticmethod
    def get_reply(user_answers):
        end = False
        if user_answers and len(user_answers) == 1:
            return 'Enter next currency', end
        elif user_answers and len(user_answers) == 2:
            answer = get_currency_rate(*user_answers)
            end = True
            return answer, end
        else:
            return 'error', end


def get_currency_rate(base, to):
    key = 'cfc531b3eb8e10ff5207673e'
    url = 'https://v3.exchangerate-api.com/pair/{key}/{base}/{to}'.format(key=key,
                                                                          base=base.upper(),
                                                                          to=to.upper())
    response = requests.get(url)
    data = response.json()
    if data.get('result') == 'success':
        rate = data.get('rate')
        return '{0} to {1} > {2}'.format(base.upper(), to.upper(), rate)
    return 'Something went wrong, try again'


if __name__ == '__main__':
    print(get_currency_rate('uah', 'usd'))
