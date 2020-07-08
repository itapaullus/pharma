import pandas as pd
from psycopg2 import extensions
from psycopg2.extras import DictCursor

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
    def get(conn: extensions.connection, label):
        # лезем в таблицу и возвращаем ID
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("select * from region where label = %s", (label))
            print(cursor)
            for row in map(dict, cursor):
                print(row)
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
