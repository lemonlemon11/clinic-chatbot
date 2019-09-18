import uuid
import TimeslotService.DTO.Text as text
import json
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
        return text.getSimpleTextDTO(appointment_id)

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
        html += '<tr><th>Doctor name</th><th>Office</th><th>Specialization</th><th>Appointment ID</th><th>Operation</th></tr>'
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
        return html

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
                doctorConn.update({'doctor_id': doctor_id}, {'$set': {'timetable': start_time_num+','}})
            else:
                doctorConn.update({'doctor_id': doctor_id}, {'$set': {'timetable': ','+start_time_num}})

        textDTO=text.getSimpleTextDTOForCancelAppointment()
        obj = json.dumps(textDTO)
        a = json.loads(obj)
        return a