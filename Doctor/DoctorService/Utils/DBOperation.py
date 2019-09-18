import DoctorService.Utils.DBConnection as dbConnect

import uuid
from pymongo import MongoClient
import json


def insertDoctor():
    conn=dbConnect.getDBConnection()
    names=['tony','jenny','gogo']
    location=['301','302','303']
    specialization=['Orthodontics','Oral Surgery','Teeth check']
    information=['aa','bb','cc']
    gender=['male','female','male']
    timetable='9,10,11,12,13,14,15,16'
    d=dict()
    for index in range(len(names)):
        d['doctor_id']=str(uuid.uuid1()).replace('-','')
        d['doctor_name']=names[index]
        d['location']=location[index]
        d['specialization']=specialization[index]
        d['gender']=gender[index]
        d['timetable']=timetable
        d['information']=information[index]
        print(d)
        obj=json.dumps(d)
        conn.insert(json.loads(obj))
insertDoctor()