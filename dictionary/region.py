import pandas as pd
from psycopg2 import extensions
from psycopg2.extras import DictCursor

gid = 0


class Region:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.label = kwargs.get('label')
        self.synonyms = set(kwargs.get('synonyms', []) + [self.label])


class Regions(list):
    def __init__(self, path=None):
        super(Regions, self).__init__()
        df = pd.read_excel(path)
        for i in df.to_records():
            self.append(Region(label=i[1], synonyms=list(i)[1:]))


class DBRegion:
    @staticmethod
    def find(conn: extensions.connection, label):   # на вход получаем соединение с БД и лейбл нужного региона для поиска
        # лезем в таблицу и возвращаем ID
        with conn.cursor(cursor_factory=DictCursor) as cursor:  # устанавливаем контекст. Это можно пока просто как правило считать
            cursor.execute("select * from region where label = %s", (label, )) # выполняем запрос
            if cursor: # если есть результаты в датасете...
                for row in map(dict, cursor): # проходим по ним датасету в цикле, преобразовывая каждую его строку в словарь
                    return Region(id=row['id'], label=row['label'], synonyms=DBRegion.get_synonyms(conn, row['id'])) # возвращаем сразу первую строку, так как больше одной строки с одним названием быть не может
        return None

    @staticmethod
    def get_synonyms(conn: extensions.connection, id):
        synonyms = []
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("select * from region_synonyms where region_id = %s", (id, ))
            if cursor:
                for row in map(dict, cursor):
                    synonyms.append(row.get('synonym'))
            return synonyms

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
