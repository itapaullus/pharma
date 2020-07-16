from postgre_engine import SQL
import pandas as pd
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
        # vallist = ", ".join([f"'{col}'" for col in kwargs.values()])
        vallist = ",".join([f"'{col[1]}'" for col in kwargs.items() if col[0] != 'table'])
        collist = ",".join(col for col in kwargs.keys() if col != 'table')
        stmt = f'insert into {kwargs.get("table", cls.tablename)} ({collist}) values ({vallist}) returning id'
        new_id = SQL.insert(stmt=stmt, **kwargs)
        return new_id

    @classmethod
    def commit(cls):
        SQL.commit()

    @classmethod
    def rollback(cls):
        SQL.rollback()


class BaseExcel:
    def __init__(self, path):
        df = pd.read_excel(path)
        self.xls = []
        for row in df.to_records():
            self.xls.append([col for col in list(row)[1:-1]])
        logger.debug(self.xls)
