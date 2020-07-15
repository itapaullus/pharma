import requests as r
import json
from dadata import Dadata


class MyDadata:
    _TOKEN = 'e2f762391c5d378c95cbacfc255d4a4dd696b3a7'
    _URL_INN = 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/party'
    _SECRET = '2df414e3088b641ab955285c4c2937acb982e34a'
    @classmethod
    def get_client_by_inn(cls, inn):
        try:
            resp = r.post(cls._URL_INN,
                        data=json.dumps({
                            "query": inn
                        }),
                        headers={
                            'Authorization': 'TOKEN '+cls._TOKEN,
                            'Content-Type': 'application/json',
                            'Accept': 'application/json'
                        }
                        )
            return resp.json().get('suggestions')[0].get('value')
        except:
            print('Сервис недоступен')
            return None

    @classmethod
    def formataddress(cls, text):
        dadata = Dadata(cls._TOKEN, cls._SECRET)
        return dadata.clean("address", text)

# request = Dadata.get_client_by_inn("7707083893")
# print(request)


print(MyDadata.formataddress('перервинский бульвар 2-1-69'))
print(MyDadata.get_client_by_inn('7707083893'))
