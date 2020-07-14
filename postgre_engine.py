import psycopg2
from dictionary import region


def main():
    conn = psycopg2.connect(dbname='ewwpaullus', user='ewwpaullus',
                            password='tkMsD2fuu4U2NR', host='pg2.sweb.ru')

    reg = region.DBRegion.find(conn, 'test regions')
    print(reg.label)
    print(reg.id)
    print(reg.synonyms)

main()