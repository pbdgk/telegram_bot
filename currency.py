import requests


def get_currency_rate(from_, to, db):
    url = 'https://v3.exchangerate-api.com/pair/{key}/{from_}/{to}'.format(key=db.get_value('weather_api'),
                                                                           from_=from_,
                                                                           to=to)
    response = requests.get(url)
    data = response.json()
    if data.get('result') == 'success':
        rate = data.get('rate')
        msg = '{0} to {1} > {2}'.format(from_, to, rate)
    else:
        msg = 'Something went wrong, try again'
    return msg


