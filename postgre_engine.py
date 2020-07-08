import psycopg2
from dictionary import region


def main():
    conn = psycopg2.connect(dbname='ewwpaullus', user='ewwpaullus',
                            password='tkMsD2fuu4U2NR', host='pg2.sweb.ru')

    region.DBRegion.get(conn, 'test')

main()