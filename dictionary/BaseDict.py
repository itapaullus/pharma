import psycopg2
from psycopg2 import extensions
from psycopg2.extras import DictCursor


class Base:
    tablename = None
    mainconn = psycopg2.connect(dbname='ewwpaullus', user='ewwpaullus',
                                password='tkMsD2fuu4U2NR', host='pg2.sweb.ru')
    @classmethod
    def select(cls, conn: extensions.connection = mainconn, **kwargs):
        with conn.cursor(cursor_factory=kwargs.get('cursor_factory', DictCursor)) as cursor:
            whereclause, topclause = '', ''
            if kwargs.get('where'):
                whereclause = f' where {kwargs.get("where")}'
            if kwargs.get('top'):
                topclause = 'LIMIT {}'.format(kwargs.get('top'))
            stmt = f'select * from {cls.tablename} {whereclause} {topclause}'
            cursor.execute(stmt)
            return {row.get('id'): row for row in map(dict, cursor)}

    @classmethod
    def insert(cls, conn: extensions.connection = mainconn, **kwargs):
        vallist = []
        stmt = f'insert into {cls.tablename} ({",".join(kwargs.keys())}) values ({",".join(kwargs.values())})'
        with conn.cursor(cursor_factory=kwargs.get('cursor_factory', DictCursor)) as cursor:
            try:
                cursor.execute(stmt)
                conn.commit()
            except Exception as e:
                print(e)




class Region(Base):
    tablename = 'region'


# print(Region.find(where='id = 4'))
print(Region.insert(label='test kim'))
