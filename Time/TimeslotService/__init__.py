from flask import Flask
from flask import request
from flask_restplus import Resource, Api
from flask_restplus import fields
import json
from flask import make_response,jsonify
from pymongo import MongoClient
import uuid
import requests



app=Flask(__name__)
api= Api(app,default="Timeslots Service", title="Timeslots Service", description="Data Service for Timeslots Services.")

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

    def checkAppointment(self,timeslotConn,user_id):
        user_timeslots=timeslotConn.find({'user_id':user_id})
        dataDict=dict()
        l=[]
        for timeslot in user_timeslots:
            d=dict()
            d['doctor_id']=timeslot['doctor_id']
            d['doctor_name'] = timeslot['doctor_name']

            d['location']=timeslot['location']
            d['appointment_time'] = timeslot['appointment_time']
            d['appointment_id']=timeslot['appointment_id']

            l.append(d)
        html = '<p>Appointment list is shown below</p>'
        html +='<table class="table table-striped table-bordered table-hover table-condensed">'
        html += '<tr><th>Doctor name</th><th>Office</th><th>Specialization</th>Time<th>Appointment ID</th><th>Operation</th></tr>'
        for doctor in l:
            appointment_id=doctor['appointment_id']
            appointment_time=doctor['appointment_time']
            doctor_id=doctor['doctor_id']
            html += '<tr>'
            for key in doctor.keys():
                if key!='doctor_id':
                    html += '<td>' + doctor[key] + '</td>'
            html+="<td><button class='btn btn-sm btn-primary' onclick=f1('"+appointment_id+"','"+appointment_time+"','"+doctor_id+"')>click to cancel</button></td>"
            html += '</tr>'
        html += '</table>'
        return html,l

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





timeslotConn=getTimeslotDBConnection()
doctorConn=getDoctorDBConnection()

collection_name='Timeslots'


input_paylod_model = api.model('data', {
    'doctor_id': fields.String,
    'appointment_time': fields.String,
    'location': fields.String,
    'user_id':fields.String,
    'doctor_name':fields.String
})

input_paylod_model2 = api.model('data2', {
    'appointment_id': fields.String,
    'doctor_id': fields.String,
    'appointment_time': fields.String,
})
@api.route('/{collection}/bookAppointment'.format(collection=collection_name),methods=['POST'])
class BookAppointment(Resource):
    @api.expect(input_paylod_model,validate=True)
    @api.doc(description="Timeslot")
    @api.response(200, 'Appointment has been booked successfully')
    @api.response(404, 'url error')
    @api.response(500, 'internal errors')
    def post(self):
        data=(json.loads(request.get_data()))
        print(data)
        # res=make_response(jsonify(data=doctor_id),200)
        # return res
        obj = TimeslotServices()
        v=obj.bookDentistsAppointment(doctorConn,timeslotConn,data)
        res=make_response(jsonify(data=v),200)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res

@api.route('/{collection}/checkAppointment/<string:user_id>'.format(collection=collection_name))
class CheckAppointment(Resource):

    @api.doc(description="Timeslot")
    @api.response(200, 'Appointment has been booked successfully')
    @api.response(404, 'url error')
    @api.response(500, 'internal errors')
    def get(self,user_id):
        session = requests.session()
        session.keep_alive = False
        obj=TimeslotServices()
        a,l=obj.checkAppointment(timeslotConn,user_id)
        print(a)
        d=dict()
        d['data']=a
        d['content']=l
        res = make_response(jsonify(d), 200)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res

@api.route('/{collection}/cancelAppointmentByAppointmentID'.format(collection=collection_name))
class CancelAppointmentByAppointmentID(Resource):
    @api.expect(input_paylod_model2,validate=True)
    @api.doc(description="Timeslot")
    @api.response(200, 'Appointment has been canceled successfully')
    @api.response(404, 'url error')
    @api.response(500, 'internal errors')
    def post(self):
        data=(json.loads(request.get_data()))
        print(data)
        obj=TimeslotServices()
        a=obj.cancelAppointmentByAppointmentID(doctorConn,timeslotConn,data)
        res = make_response(jsonify(data=a), 200)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res


if __name__=='__main__':
    app.run(host='0.0.0.0')
    # app.run(host='0.0.0.0',debug=True,port=9999)