
import requests
from global_modules.exeptions import CodeDataException


def get_field_in_dict_or_exception(data: dict, field, message, code=400):
    if data.get(field):
        return data[field]
    else:
        raise CodeDataException(error=message, status=code)
    

class Converter:

    ids = ""
    vs_currencies = ""


    def convert_to_xmr(self):
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": self.ids,
            "vs_currencies": self.vs_currencies
        }

        # Отправляем GET-запрос к API CoinGecko
        response = requests.get(url, params=params)

        # Парсим JSON-ответ
        data = response.json()
        print(data)
        # Извлекаем цену Monero в рублях
        xmr_price_in_rub = data[self.ids]["rub"]
        return xmr_price_in_rub