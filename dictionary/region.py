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
    def find(conn: extensions.connection, label):
        # лезем в таблицу и возвращаем ID
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("select * from region where label = %s", (label, ))
            if cursor:
                for row in map(dict, cursor):
                    return Region(id=row['id'], label=row['label'], synonyms=DBRegion.get_synonyms(conn, row['id']))
        return None

    @staticmethod
    def get_synonyms(conn: extensions.connection, id):
        synonyms = []
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            print(id)
            cursor.execute("select * from region_synonyms where region_id = %s", (id, ))
            if cursor:
                print(cursor)
                for row in map(dict, cursor):
                    print(row)
                    synonyms.append(row.get('label'))
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
