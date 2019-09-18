from pymongo import MongoClient

def getTimeslotDBConnection():
    db_name='comp9322'
    collection='Timeslot'
    client = MongoClient("mongodb://root:ltf9495!@ds117866.mlab.com:17866/{db}".format(db=db_name))
    db = client[db_name]
    c = db[collection]
    return c

def getDoctorDBConnection():
    db_name='comp9322'
    collection='Doctor'
    client = MongoClient("mongodb://root:ltf9495!@ds117866.mlab.com:17866/{db}".format(db=db_name))
    db = client[db_name]
    c = db[collection]
    return c


