import dictionary.region as r
if __name__ == '__main__':
    r = r.DBRegion.get(label='tests regions')
    print(r)
