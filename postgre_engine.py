import psycopg2

conn = psycopg2.connect(dbname='ewwpaullus', user='ewwpaullus',
                        password='tkMsD2fuu4U2NR', host='pg2.sweb.ru')
cursor = conn.cursor()
