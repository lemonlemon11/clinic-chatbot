from pymongo import MongoClient

def getDBConnection():
    db_name='comp9322'
    collection='Doctor'
    client = MongoClient("mongodb://root:ltf9495!@ds117866.mlab.com:17866/{db}".format(db=db_name))
    db = client[db_name]
    c = db[collection]
    return c

def test():
    return 111

