import json
import requests
from config import exchanges


class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            raise APIException(f"Валюта {sym} не найдена!")

        if base_key == sym_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        r = requests.get(f"https://api.freecurrencyapi.com/v1/latest?apikey=M1DIkh1yxVhTX3VWrJoKlbzuPbSZqzzT19k66OeC&currencies={base_key}%2C{sym_key}")
        resp = json.loads(r.content)
        if base_key == 'RUB':
            new_price = amount / resp['data'][base_key]
            new_price = round(new_price, 3)
            message = f"Цена {amount} {base} в {sym} : {new_price}"
        else:
            new_price = resp['data'][sym_key] * amount
            new_price = round(new_price, 3)
            message = f"Цена {amount} {base} в {sym} : {new_price}"
        return message
