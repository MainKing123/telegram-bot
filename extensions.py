import requests
import json
class APIException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        try:
            amount = float(amount)
        except ValueError:
            raise APIException("Неверное количество валюты")

        if base == quote:
            raise APIException("Невозможно конвертировать одинаковые валюты")

        try:
            response = requests.get(f'https://api.exchangerate-api.com/v4/latest/{base}')
            rates = json.loads(response.content)['rates']
            
            if quote not in rates:
                raise APIException(f"Валюта {quote} не найдена")
                
            return rates[quote] * amount
            
        except requests.exceptions.RequestException:
            raise APIException("Ошибка при получении курса валют")

