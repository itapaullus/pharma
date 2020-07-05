import pandas as pd
import ext_api


df = pd.read_excel('data/Clients.xlsx', 'Клиенты')

for i in df.to_records():
    if not i[1]:
        x = 1
    else:
        ph_name = ext_api.Dadata.get_client_by_inn(str(i[2]))
        print(ph_name)
        #inn.update({a: ph_name})
        #inn.to_csv('data/Client.csv', sheet_name='Лист1')
