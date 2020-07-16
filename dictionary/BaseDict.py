import psycopg2
from psycopg2 import extensions
from postgre_engine import SQL
import Log

logger = Log.Logger('BASEDICT')


class Base:
    tablename = None
    logger = Log.Logger('BASEDICT.BASE')  # logger класса

    @classmethod
    def select(cls, **kwargs):
        whereclause, topclause = '', ''
        if kwargs.get('where'):
            whereclause = f'where {kwargs.get("where")}'
        if kwargs.get('top'):
            topclause = 'LIMIT {}'.format(kwargs.get('top'))
        stmt = f'select * from {kwargs.get("table", cls.tablename)} {whereclause} {topclause}'
        cursor = SQL.select(stmt=stmt, **kwargs)
        return {row.get('id'): row for row in cursor}

    @classmethod
    def insert(cls, **kwargs):
        vallist = ", ".join([f"'{col}'" for col in kwargs.values()])
        stmt = f'insert into {cls.tablename} ({",".join(kwargs.keys())}) values ({vallist}) returning id'
        new_id = SQL.insert(stmt=stmt, **kwargs)
        return new_id


class Test(Base):
    tablename = 'test'

    @classmethod
    def select(cls, **kwargs):
        return super(Test, cls).select(**kwargs)



if __name__ == '__main__':
    try:
        print(Test.select(where="label = 'test kim'"))
        print(Test.insert(label = 'myNewRegion'))
    except Exception as e:
        logger.exception(e)
