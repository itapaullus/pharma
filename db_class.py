import pandas as pd
import ext_api

gid = 0
class Region:
    def __init__(self, label, args):
        self.label = label
        self.synonyms = set(list(args) + [label])

class Regions(list):
    def __init__(self, path=None):
        super(Regions, self).__init__()
        df = pd.read_excel(path)
        for i in df.to_records():
            self.append(Region(i[1], list(i)[1:]))

class DBRegion:
    @staticmethod
    def get(label):
        # лезем в таблицу и возвращаем ID
        return None

    @staticmethod
    def save_synonyms(id, synonyms):
        print(f'Сохранили {id} {synonyms}')

    @staticmethod
    def save_region(label):
        global gid
        gid += 1
        print(f'Сохранили регион {gid} - {label}')
        return gid

    @staticmethod
    def getlist():
        return Regions()

class Client:
    def __init__(self, inn, label = ''):
        self.inn = inn
        if label:
            self.label = label
        else:
            self.label = ext_api.Dadata.get_client_by_inn(inn)


class DBClient:
    @staticmethod
    def get():
        pass

