import pandas as pd
import db_class as db
import db_class2 as db2
import db_class3 as db3

RegList = db.Regions('Regions.xlsx')
for i in RegList:
    # print(i.label)
    # print(i.synonyms)
    regionid = db.DBRegion.get(i.label)
    if regionid:
        db.DBRegion.save_synonyms(regionid, i.synonyms)
    else:
        newid = db.DBRegion.save_region(i.label)
        db.DBRegion.save_synonyms(newid, i.synonyms)

List = db2.Products('Product.xlsx')
for i in List:
    # print(i.label)
    # print(i.synonyms)
    productid = db2.DBProduct.get(i.label)
    if productid:
        db2.DBProduct.save_synonyms(productid, i.synonyms)
    else:
        newid = db2.DBProduct.save_product(i.label)
        db2.DBProduct.save_synonyms(newid, i.synonyms)
        db2.DBProduct.save_eng(i.engname)


List = db3.Distribs('Distributors.xlsx')
for i in List:
    # print(i.label)
    # print(i.synonyms)
    distribid = db3.DBDistrib.get(i.label)
    if distribid:
        db3.DBDistrib.save_distrib(distribid, i.label)
    else:
        newid = db3.DBDistrib.save_distrib(i.label)
        db3.DBDistrib.save_eng(i.engdist)