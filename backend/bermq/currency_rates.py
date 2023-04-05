import requests
from datetime import date, timedelta

def get_rates(symbols, base='BTC'):
    url = f'https://api.exchangerate.host/latest?base={base}&symbols={",".join(symbols)}'
    response = requests.get(url)
    data = response.json()
    current_rates = data['rates']
    previous_day = str(date.fromisoformat(data['date']) - timedelta(days=1))
    url = f'https://api.exchangerate.host/{previous_day}?base={base}&symbols={",".join(symbols)}'
    response = requests.get(url)
    previous_rates = response.json()['rates']
    return current_rates, previous_rates
