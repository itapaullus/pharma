import dictionary.region as region

if __name__ == '__main__':
    # r = region.DBRegion.get(label='test kim')
    # print(r)
    # new = region.DBRegion.save('italnc')
    # print(new)
    # BD.Test(r'data\Regions.xlsx')
    reg = region.ExcelRegion(r'data\Regions.xlsx')
    reg.savetodb()
