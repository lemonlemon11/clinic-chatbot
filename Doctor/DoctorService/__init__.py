from flask import Flask
from flask import jsonify
from flask import make_response
from flask_restplus import Resource, Api
# import DoctorService.Services.DoctorServices as doctorService
import json
from pymongo import MongoClient
import random



def timetableToTimeSlot(timetable):
    timeslot_list = []

    if timetable.find(',')!=-1:
        timetable_list=timetable.split(',')
        for times in timetable_list:
            d = dict()
            whole_time_str_start=times+':00'
            whole_time_str_end=str(int(times)+1)+':00'
            d['start_time']=whole_time_str_start
            d['end_time']=whole_time_str_end
            timeslot_list.append(d)
        return timeslot_list
    elif len(timetable)==0:
        return None
    else:
        d = dict()
        whole_time_str_start =  timetable + ':00'
        whole_time_str_end = str(int(timetable) + 1) + ':00'
        d['start_time'] = whole_time_str_start
        d['end_time'] = whole_time_str_end
        timeslot_list.append(d)
        return timeslot_list




class DoctorServices:
    def greeting_response(self):
        list=['hi','hello','hi human','hello human','hi there','hello there','hey','hey there']
        length=len(list)
        index=random.randint(0,length-1)
        return list[index]

    def getAllDoctor(self,conn):
        doctor_list=conn.find()
        l=[]
        for values in doctor_list:
            d=dict()
            d['doctor_name']=values['doctor_name']
            d['location']=values['location']
            d['specialization']=values['specialization']
            l.append(d)
        doctorList=dict()
        doctorList['content']=l
        html='<p>Doctor list is shown below</p>'
        html += '<table class="table table-striped table-bordered table-hover table-condensed">'
        html+='<tr><th>Doctor name</th><th>Office</th><th>Specialization</th></tr>'
        for doctor in l:
            print(doctor)
            html+='<tr>'
            for key in doctor.keys():
                html+='<td>'+doctor[key]+'</td>'
            html+='</tr>'
        html+='</table>'
        html+='</br>'
        html+="<p>You can enter 'doctor name + information' to get doctor's information (eg. James information)</p>"
        doctorList['data']=html
        obj=json.dumps(doctorList)
        a=json.loads(obj)
        # print(a)
        return a


    def getDoctorInformationByDoctorName(self,conn,doctor_name):
        values=conn.find_one({'doctor_name':doctor_name})
        print(values)
        v=dict()
        for key in values.keys():
            if key!='_id':
                v[key]=values[key]
        result='<p>This is Doctor '+doctor_name+' introduction:</p>'+'<p>'+values['information']+'</p>'
        obj = json.dumps(result)
        print(obj)
        return (json.loads(obj)),v

    def getAvailableTimeslotsByDoctorName(self,doctor_name,conn):
        print(doctor_name)
        values=conn.find_one({'doctor_name':doctor_name})
        print(values)
        d=dict()
        doctor_id = values['doctor_id']
        # doctor_name = values['doctor_name']
        information= values['information']
        specialization= values['specialization']
        location= values['location']
        v=dict()
        v['doctor_id']=doctor_id
        v['information']=information
        v['specialization']=specialization
        v['location']=location

        html='<p>'+doctor_name+'<p>'
        html+= '<p>Information: '+information+'<p>'
        html+= '<p>Location: '+location+'<p>'
        html+= '<p>Specialization: '+specialization+'<p>'
        html+='<table class="table table-striped table-bordered table-hover table-condensed">'
        html+='<tr><th>start time</th><th>end time</th><th>book appointment</th></tr>'

        doctor_timetable=values['timetable']
        v['timetable'] = doctor_timetable

        if doctor_timetable=='':
            result = dict()
            msg_option = 'No available timeslot'
            msg_option += 'Please type these questions to continue your service'
            msg_option += '<ul>'
            msg_option += '<li>show dentist list</li>'
            msg_option += '<li>list available dentists</li>'
            msg_option += '<li>check my appointments</li>'
            msg_option += '<li>list available timeslot of + (doctor name)</li>'
            msg_option += '<li>(doctor name) + information</li>'
            msg_option += '</ul>'
            result['data'] = msg_option

            obj = json.dumps(result)
            b = (json.loads(obj))
            return b
        time_slots=timetableToTimeSlot(doctor_timetable)
        for time in time_slots:
            html+='<tr>'
            appointment_time=time['start_time']+'-'+time['end_time']
            print(appointment_time)
            for key in time.keys():
                html+='<td>'+time[key]+'</td>'
            html+="<td><button class='btn btn-sm btn-primary' onclick=f('"+appointment_time+"','"+location+"','"+doctor_id+"','"+doctor_name+"')>click to book</button></td>"
            # html+="<td><button class='btn btn-sm btn-primary' onclick=f('"+appointment_time+"','"+location+"')>click to book</button></td>"
            html+='</tr>'
        html+='please select one following timeslot and click the button to book your appointment'
        # html+='<input type="text" value="'+doctor_id+'" id="doctor_id">'
        # html+='<input type="text" value="'+doctor_name+'" id="doctor_name">'
        d['timetable']=time_slots
        result=dict()
        result['data']=html
        result['content']=v

        # a=text.getTimeslotsTextDTO(result)
        obj = json.dumps(result)
        b=(json.loads(obj))
        return b




    def getAvailableDentists(self,conn):
        l=[]
        doctor_list=conn.find()
        print(doctor_list)
        for values in doctor_list:
            timetable=values['timetable']
            if len(timetable)!=0:
                d=dict()
                # d['doctor_id'] = values['doctor_id']
                d['doctor_name'] = values['doctor_name']
                d['information'] = values['information']
                d['location'] = values['location']
                d['specialization']=values['specialization']
                # doctor_timetable = values['timetable']
                # print(doctor_timetable)
                # time_slots = timeslot.timetableToTimeSlot(doctor_timetable)
                # d['timetable'] = time_slots
                l.append(d)

        if len(l)!=0:
            result = dict()
            result['data'] = l
            # result = gallery.getGalleryDTO(result)

            doctorList = dict()
            html = '<p>Available doctor list is shown below</p>'
            html += '<table class="table table-striped table-bordered table-hover table-condensed">'
            html += '<tr><th>Doctor name</th><th>Information</th><th>Office</th><th>Specialization</th></tr>'
            dl=[]
            for doctor in l:
                print(doctor)
                dl.append(doctor)
                html += '<tr>'
                for key in doctor.keys():
                    html += '<td>' + doctor[key] + '</td>'
                html += '</tr>'
            html += '</table>'
            html += '</br>'
            html += "<p>You can enter 'doctor name + timeslot' to check the available timeslot (eg. James timeslot)</p>"
            doctorList['data'] = html
            doctorList['content']=dl
            obj = json.dumps(doctorList)
            a = json.loads(obj)
            print(a)
            return a

        else:
            result = dict()
            result['data'] = 'Sorry, No available doctor.'
            obj = json.dumps(result)
            a = json.loads(obj)
            return a







def getDBConnection():
    db_name='comp9322'
    collection='Doctor'
    client = MongoClient("mongodb://root:ltf9495!@ds117866.mlab.com:17866/{db}".format(db=db_name))
    db = client[db_name]
    c = db[collection]
    return c






app=Flask(__name__)
api= Api(app,default="Dentist Service", title="Doctor Service", description="Data Service for Dentist Services.")

conn=getDBConnection()

collection_name='Doctors'

@api.route('/{collection}/greeting/<string:greeting>'.format(collection=collection_name))
class greeting(Resource):
    @api.doc(description="Common greeting ")
    @api.response(200, 'response successfully')
    @api.response(404, 'url error')
    @api.response(500, 'internal errors')
    def get(self,greeting):
        obj=DoctorServices()

        a=(obj.greeting_response())
        res = make_response(jsonify(data=a), 200)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res

@api.route('/{collection}/getDentistInformationByName/<string:doctor_name>'.format(collection=collection_name))
class GetDentistInformationByName(Resource):
    @api.doc(description="Get dentist personal information by dentist's name")
    @api.response(200, 'retrieve successfully')
    @api.response(404, 'url error')
    @api.response(500, 'internal errors')
    def get(self,doctor_name):
        name=doctor_name
        # name=request.args.get('data')
        print(name)
        # doctorService=DoctorServices()
        obj=DoctorServices()

        a,values=(obj.getDoctorInformationByDoctorName(conn,name))
        d=dict()
        d['content']=values
        d['data']=a
        res = make_response(jsonify(d), 200)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res

@api.route('/{collection}/getAllDoctors'.format(collection=collection_name))
class GetAllDoctors(Resource):
    @api.doc(description="Get all Dotors information")
    @api.response(200, 'retrieve successfully')
    @api.response(404, 'url error')
    @api.response(500, 'internal errors')
    def get(self):
        obj=DoctorServices()

        doctor_list=obj.getAllDoctor(conn)
        obj = json.dumps(doctor_list)
        a = json.loads(obj)
        res=make_response(jsonify(a),200)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res



@api.route('/{collection}/getAvailableTimeslotByName/<string:doctor_name>'.format(collection=collection_name))
class GetAvailableTimeslotsByName(Resource):
    @api.doc(description="Get available timeslots for each dentist")
    @api.response(200, 'retrieve successfully')
    @api.response(404, 'url error')
    @api.response(500, 'internal errors')
    def get(self,doctor_name):
        # name = request.args.get('data')
        name=doctor_name
        print(name)
        obj=DoctorServices()

        doctor_list=obj.getAvailableTimeslotsByDoctorName(name, conn)
        obj = json.dumps(doctor_list)
        a = json.loads(obj)
        res = make_response(jsonify(a), 200)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res

@api.route('/{collection}/getAvailableDentist'.format(collection=collection_name))
class GetAvailableDentist(Resource):
    @api.doc(description="Get available dentist")
    @api.response(200, 'retrieve successfully')
    @api.response(404, 'url error')
    @api.response(500, 'internal errors')
    def get(self):
        obj=DoctorServices()

        doctor_list = obj.getAvailableDentists(conn)
        obj = json.dumps(doctor_list)
        a = json.loads(obj)
        res = make_response(jsonify(a), 200)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res


# @api.route('/{collection}/getAvailableTimesoltsForEachDentistInQuickReply/<string:doctor_id>'.format(collection=collection_name))
# class GetAvailableTimeslotsByDoctorIDInQuickReply(Resource):
#     @api.doc(description="Get available timeslots for each dentist")
#     @api.response(200, 'retrieve successfully')
#     @api.response(404, 'url error')
#     @api.response(500, 'internal errors')
#     def get(self, doctor_id):
#         obj = doctorService.DoctorServices()
#         return obj.getAvailableTimeslotsByDoctorIDInQuickReply(doctor_id, conn)


if __name__=='__main__':
    app.run(host='0.0.0.0')
    # app.run(host='0.0.0.0',debug=True,port=7777)