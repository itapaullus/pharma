import pandas as pd
from psycopg2 import extensions
from psycopg2.extras import DictCursor

gid = 0


class Region:
    def __init__(self, **kwargs):
        if kwargs.get('id'):
            self.id = kwargs.get('id')
            self.label = kwargs.get('label')
            self.synonyms = set(kwargs.get('synonyms', []) + [self.label])
        else:
            conn = kwargs.get('connection')
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.select("select * from region where id = %s", (kwargs.get('id'),))
                if cursor:
                    for row in map(dict, cursor):
                        self.id = row.get('id')
                        self.label = row.get('label')
                        self.synonyms = DBRegion.get_synonyms(conn, row['id'])


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
            cursor.select("select * from region where label = %s", (label,)) # выполняем запрос
            if cursor:  # если есть результаты в датасете...
                print(cursor)
                for row in map(dict, cursor):  # проходим по ним датасету в цикле, преобразовывая каждую его строку в словарь
                    print(41)
                    return Region(id=row['id'], label=row['label'], synonyms=DBRegion.get_synonyms(conn, row['id'])) # возвращаем сразу первую строку, так как больше одной строки с одним названием быть не может
            else: # если результатов нет, поищем в синонимах
                print('Ищем в синонимах')
                cursor.select("select * from region_synonyms where synonym = %s", (label,))
                if cursor:
                    for row in map(dict, cursor):
                        return Region(id=row['region_id'], label=row['label'], synonyms=DBRegion.get_synonyms(conn, row['id']))
        return None

    @staticmethod
    def get_synonyms(conn: extensions.connection, id):
        synonyms = []
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.select("select * from region_synonyms where region_id = %s", (id,))
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
