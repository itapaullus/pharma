import pandas as pd

gid = 0

class Distrib:
    def __init__(self, label, engdist):
        self.label = label
        self.engdist = engdist


class Distribs(list):
    def __init__(self, path=None):
        super(Distribs, self).__init__()
        df = pd.read_excel(path)
        for i in df.to_records():
            self.append(Distrib(i[1], list(i)[2]))

class DBDistrib:
    @staticmethod
    def get(label):
        # лезем в табоицу и возвращаем ID
        return None

    @staticmethod
    def save_eng(engdist):
        print(f'Save EnName - {engdist}')

    @staticmethod
    def save_distrib(label):
        global gid
        gid += 1
        print(f'Сохранили дистрибьютора {gid} - {label}')
        return gid

    @staticmethod
    def getlist():
        return Distribs()


#List = Distribs('Distributors.xlsx')
#for i in List:
    # print(i.label)
    # print(i.synonyms)
   # distribid = DBDistrib.get(i.label)
    #if distribid:
     #   DBDistrib.save_distrib(distribid, i.label)
    #else:
       # newid = DBDistrib.save_distrib(i.label)
       # DBDistrib.save_eng(i.engdist)