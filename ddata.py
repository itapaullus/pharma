import json

import requests

import pandas as pd



API_KEY = '0029fc44f41050eb57d459826f5a0573c944e3ed'
BASE_URL = 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/'




xl = pd.read_excel('Clients.xlsx')


def suggest(query, resource):
    url = BASE_URL + resource
    headers = {
        'Authorization': 'Token ' + API_KEY,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    data = {
        'query': query
    }
    res = requests.post(url, data=json.dumps(data), headers=headers)
    return res.json()

class Inn:
    def __init__(self, label):
        self.label = label

class Inns(list):
    def __init__(self, path=None):
        super(Inn, self).__init__()
        df = pd.read_excel(path)
        for i in df.to_records():
            self.append(Inn(i[2]))

class DBInn:

    @staticmethod
    def save_inn(label):
        print(f'Сохранил - {label}')



for i in xl:
    DBInn.save_inn(i.label)


