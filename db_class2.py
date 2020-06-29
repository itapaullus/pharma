import pandas as pd

gid = 0


class Product:
    def __init__(self, label, args):
        self.label = label
        self.synonyms = set(list(args) + [label])


class Products(list):
    def __init__(self, path=None):
        super(Products, self).__init__()
        df = pd.read_excel(path)
        for i in df.to_records():
            self.append(Product(i[1], list(i)[1:]))


class DBProduct:
    @staticmethod
    def get(label):
        # лезем в табоицу и возвращаем ID
        return None

    @staticmethod
    def save_synonyms(id, synonyms):
        print(f'Сохранили {id} {synonyms}')

    @staticmethod
    def save_product(label):
        global gid
        gid += 1
        print(f'Сохранили продукт {gid} - {label}')
        return gid

    @staticmethod
    def getlist():
        return Products()


List = Products('Product.xlsx')
for i in List:
    # print(i.label)
    # print(i.synonyms)
    productid = DBProduct.get(i.label)
    if productid:
        DBProduct.save_synonyms(productid, i.synonyms)
    else:
        newid = DBProduct.save_product(i.label)
        DBProduct.save_synonyms(newid, i.synonyms)
