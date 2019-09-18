from flask import Flask,jsonify,make_response
from flask import render_template
from flask_cors import *
from flask import request
import requests
import json
import uuid
from pymongo import MongoClient
from datetime import timedelta
app = Flask(__name__)
CORS(app, resources=r'/*')
# app.config['DEBUG']=True
# app.config['SEND_FILE_MAX_AGE_DEFAULT']=timedelta(seconds=1)
# app.jinja_env.auto_reload=True


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


def getSimpleTextDTOForCancelAppointment():
    msg_option = 'Appointment has been canceled successfully.</br>'
    msg_option+='Please type these questions to continue your service'
    msg_option += '<ul>'
    msg_option += '<li>show dentist list</li>'
    msg_option += '<li>list available dentists</li>'
    msg_option += '<li>check my appointments</li>'
    msg_option += '<li>list available timeslot of + (doctor name)</li>'
    msg_option += '<li>(doctor name) + information</li>'
    msg_option += '</ul>'
    return msg_option

def getSimpleTextDTO(appointment_id):
    msg_option="Appointment has been booked successfully</br>"
    msg_option+=" Your appointment id is {appointment_id}</br>".format(
        appointment_id=appointment_id)
    msg_option += 'Please type these questions to continue your service'
    msg_option += '<ul>'
    msg_option += '<li>show dentist list</li>'
    msg_option += '<li>list available dentists</li>'
    msg_option += '<li>check my appointments</li>'
    msg_option += '<li>list available timeslot of + (doctor name)</li>'
    msg_option += '<li>(doctor name) + information</li>'
    msg_option += '</ul>'
    return msg_option

class TimeslotServices:
    def bookDentistsAppointment(self,doctorConn,timeslotConn,input_payload):
        print(input_payload)
        doctor_name=input_payload['doctor_name']
        doctor_id = input_payload['doctor_id']
        user_id=input_payload['user_id']
        location = input_payload['location']
        appointment_time = input_payload['appointment_time']
        d=dict()
        d['user_id']=user_id
        d['doctor_id']=doctor_id
        d['location']=location
        d['appointment_time']=appointment_time
        d['doctor_name']=doctor_name
        appointment_id=str(uuid.uuid1()).replace('-','')

        d['appointment_id']=appointment_id
        obj = json.dumps(d)
        timeslotConn.insert(json.loads(obj))

        doctorData=doctorConn.find_one({'doctor_id':doctor_id})
        doctor_timeslot=doctorData['timetable']

        doctor_timeslot_replacement=None
        if doctor_timeslot.find(',')!=-1:
            start_time=appointment_time.split('-')[0]
            start_time_num=start_time.split(':')[0]
            last_time_num=doctor_timeslot.split(',')[-1]
            if last_time_num==start_time_num:
                doctor_timeslot_replacement=doctor_timeslot.replace(','+last_time_num,'')
            else:
                doctor_timeslot_replacement=doctor_timeslot.replace(start_time_num+',','')

        else:
            start_time = appointment_time.split('-')[0]
            start_time_num = start_time.split(':')[0]
            doctor_timeslot_replacement=doctor_timeslot.replace(start_time_num,'')

        print('doctor_timeslot_replacement',doctor_timeslot_replacement)
        doctorConn.update({'doctor_id':doctor_id},{'$set':{'timetable':doctor_timeslot_replacement}})
        return getSimpleTextDTO(appointment_id)


    def cancelAppointmentByAppointmentID(self,doctorConn,timeslotConn,input_payload):
        doctor_id = input_payload['doctor_id']

        timeslot = input_payload['appointment_time']
        appointment_id = input_payload['appointment_id']
        timeslotConn.remove({"appointment_id":appointment_id})
        doctor=doctorConn.find_one({'doctor_id':doctor_id})
        doctor_timetable=doctor['timetable']

        start_time_num = timeslot.split('-')[0].split(':')[0]
        if doctor_timetable.find(',')!=-1:
            timeslots = doctor_timetable.split(',')
            for timeslot in timeslots:
                if int(timeslot)>int(start_time_num):
                    index = (doctor_timetable.find(timeslot))

                    print(index)
                    l = list(doctor_timetable)
                    l.insert(index, start_time_num+',')
                    new_timetable=''.join(l)
                    doctorConn.update({'doctor_id': doctor_id}, {'$set': {'timetable': new_timetable}})
                    break
            else:
                new_timetable=doctor_timetable+','+start_time_num
                doctorConn.update({'doctor_id': doctor_id}, {'$set': {'timetable': new_timetable}})

        elif doctor_timetable.find(',')==-1 and len(doctor_timetable)==0:

            doctorConn.update({'doctor_id': doctor_id}, {'$set': {'timetable': start_time_num}})
        else:
            if int(doctor_timetable)>int(start_time_num):
                doctorConn.update({'doctor_id': doctor_id}, {'$set': {'timetable': start_time_num+','+doctor_timetable}})
            else:
                doctorConn.update({'doctor_id': doctor_id}, {'$set': {'timetable': doctor_timetable+','+start_time_num}})

        textDTO=getSimpleTextDTOForCancelAppointment()
        obj = json.dumps(textDTO)
        a = json.loads(obj)
        return a



@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/Timeslots/bookAppointment',methods=['POST'])
def bookAppointment():
    doctor_id = request.form.get('doctor_id')

    location = request.form.get('location')
    appointment_time = request.form.get('appointment_time')
    user_id = request.form.get('user_id')
    doctor_name = request.form.get('doctor_name')
    data=dict()
    data['doctor_id']=doctor_id
    data['location']=location
    data['appointment_time']=appointment_time
    data['user_id']=user_id
    data['doctor_name']=doctor_name

    obj = TimeslotServices()
    v = obj.bookDentistsAppointment(getDoctorDBConnection(), getTimeslotDBConnection(), data)
    print('v',v)
    res = make_response(jsonify(data=v), 200)
    res.headers['Access-Control-Allow-Origin'] = '*'

    return res

@app.route('/Timeslots/cancelAppointmentByAppointmentID',methods=['POST'])
def cancelAppointmentByAppointmentID():
    appointment_id = request.form.get('appointment_id')
    doctor_id = request.form.get('doctor_id')
    appointment_time = request.form.get('appointment_time')
    obj = TimeslotServices()
    data=dict()
    data['appointment_id']=appointment_id
    data['doctor_id']=doctor_id
    data['appointment_time']=appointment_time
    a = obj.cancelAppointmentByAppointmentID(getDoctorDBConnection(), getTimeslotDBConnection(), data)
    print('a',a)
    res = make_response(jsonify(data=a), 200)
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res


if __name__ == '__main__':
    app.run(host='0.0.0.0')
    # app.run(host='0.0.0.0',port=5002)
    # s = requests.session()
    # s.keep_alive = False
    # app.run(host='0.0.0.0',debug=True)
