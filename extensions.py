import requests
import json
from config import keys


class APIException(Exception):
    pass


class ValuesConverter:
    @staticmethod
    def converter(quote: str, base: str, amount: str):
        quote_ticker, base_ticker = keys[quote], keys[base]

        if quote == base:
            raise APIException(f'Не удалось перевести валюту')

        try:
            quote_ticker == keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {quote}')

        try:
            base_ticker == keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту: {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество: {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = round(json.loads(r.content)[keys[base]] * amount, 2)

        return total_base