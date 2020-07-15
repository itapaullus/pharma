import psycopg2
from dictionary import region
import Log
from psycopg2.extras import DictCursor


class SQL:
    logger = Log.Logger('POSTGRE_ENGINE.SQL')
    try:
        conn = psycopg2.connect(dbname='ewwpaullus', user='ewwpaullus',
                                password='tkMsD2fuu4U2NR', host='pg2.sweb.ru')
        logger.info('Connection to DB successfully set')
    except Exception as e:
        logger.error(f'Connection to DB failed: {e}')
        raise e

    @classmethod
    def select(cls, stmt, **kwargs):
        logger = Log.Logger('POSTGRE_ENGINE.SQL.SELECT')
        with cls.conn.cursor(cursor_factory=kwargs.get('cursor_factory', DictCursor)) as cursor:
            try:
                cursor.execute(stmt)
                res = [row for row in map(dict, cursor)]
                logger.info(f'{stmt}: {len(res)} rows returned.')
                return res
            except Exception as e:
                logger.exception(f'SQL ERROR: {stmt}:   {e}')
                raise

    @classmethod
    def insert(cls, stmt, **kwargs):
        logger = Log.Logger('POSTGRE_ENGINE.SQL.INSERT')
        with cls.conn.cursor() as cursor:
            try:
                cursor.execute(stmt)
                new_id = cursor.fetchone()[0]
                cls.conn.commit()
                logger.info(f'{stmt}: 1 row inserted. NewID = {new_id}')
                return new_id
            except Exception as e:
                logger.exception(f'SQL ERROR: {stmt}:   {e}')
                raise
