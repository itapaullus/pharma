import pandas as pd
import psycopg2
from psycopg2 import extensions, sql
from psycopg2.extras import DictCursor


class Base:
    tablename = None
    mainconn = psycopg2.connect(dbname='ewwpaullus', user='ewwpaullus',
                                password='tkMsD2fuu4U2NR', host='pg2.sweb.ru')
    @classmethod
    def find(cls, conn: extensions.connection = mainconn, **kwargs):
        with conn.cursor(cursor_factory=kwargs.get('cursor_factory', DictCursor)) as cursor:
            whereclause, topclause = '', ''
            if kwargs.get('where'):
                whereclause = f' where {kwargs.get("where")}'
            if kwargs.get('top'):
                topclause = 'LIMIT {}'.format(kwargs.get('top'))
            stmt = f'select * from {cls.tablename} {whereclause} {topclause}'
            cursor.execute(stmt)
            return {row.get('id'): row for row in map(dict, cursor)}


class region(Base):
    tablename = 'region'


print(region.find(top=1))




# stmt = sql.SQL('SELECT {} FROM {} LIMIT 5').format(
#             sql.SQL(',').join(map(sql.Identifier, columns)),
#             sql.Identifier('airport')
#         )



        # def find(conn: extensions.connection,
        #          label):  # на вход получаем соединение с БД и лейбл нужного региона для поиска
        #     # лезем в таблицу и возвращаем ID
        #     with conn.cursor(
        #             cursor_factory=DictCursor) as cursor:  # устанавливаем контекст. Это можно пока просто как правило считать
        #         cursor.execute("select * from region where label = %s", (label,))  # выполняем запрос
        #         if cursor:  # если есть результаты в датасете...
        #             print(cursor)
        #             for row in map(dict,
        #                            cursor):  # проходим по ним датасету в цикле, преобразовывая каждую его строку в словарь
        #                 print(41)
        #                 return Region(id=row['id'], label=row['label'], synonyms=DBRegion.get_synonyms(conn, row[
        #                     'id']))  # возвращаем сразу первую строку, так как больше одной строки с одним названием быть не может
        #         else:  # если результатов нет, поищем в синонимах
        #             print('Ищем в синонимах')
        #             cursor.execute("select * from region_synonyms where synonym = %s", (label,))
        #             if cursor:
        #                 for row in map(dict, cursor):
        #                     return Region(id=row['region_id'], label=row['label'],
        #                                   synonyms=DBRegion.get_synonyms(conn, row['id']))
        #     return None



class Newdict(Base):
    pass
