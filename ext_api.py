import requests as r
import json

class Dadata:
    _TOKEN = 'Token e2f762391c5d378c95cbacfc255d4a4dd696b3a7'
    _URL_INN = 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/party'
    @classmethod
    def get_client_by_inn(cls, inn):
        resp = r.post(cls._URL_INN,
                    data=json.dumps({
                        "query": inn
                    }),
                    headers={
                        'Authorization': cls._TOKEN,
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    }
                    )
        try:
            return resp.json().get('suggestions')[0].get('value')
        except:
            return None


request = Dadata.get_client_by_inn("7707083893")
print(request)
