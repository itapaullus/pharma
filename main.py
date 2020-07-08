from dictionary import region as db

RegList = db.Regions('data/Regions.xlsx')
for i in RegList:
    # print(i.label)
    # print(i.synonyms)
    regionid = db.DBRegion.get(i.label)
    if regionid:
        db.DBRegion.save_synonyms(regionid, i.synonyms)
    else:
        newid = db.DBRegion.save_region(i.label)
        db.DBRegion.save_synonyms(newid, i.synonyms)
