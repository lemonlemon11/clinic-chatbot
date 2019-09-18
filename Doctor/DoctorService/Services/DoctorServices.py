import DoctorService.Utils.TimetableToTimeSlot as timeslot
import json
import DoctorService.DTO.Gallery as gallery
import DoctorService.DTO.Text as text
import DoctorService.DTO.ListDTO as listDTO
import DoctorService.DTO.QuickReply as quickReply
import random
# doctor_id
# doctor_name
# location
# specialization
# gender
# timetable
# location
# information

class DoctorServices:
    def greeting_response(self):
        list=['hi','hello','hi human','hello human','hi there','hello there','hey','hey there']
        length=len(list)
        index=random.randint(0,length-1)
        return list[index]

    def getAvailableTimeslotsByDoctorIDInQuickReply(self,doctor_id,conn):
        print(doctor_id)
        data=conn.find_one({'doctor_id':doctor_id.split('_')[0]})
        print(data)
        timeslots=data['timetable']
        print(timeslots)
        time_slots = timeslot.timetableToTimeSlot(timeslots)
        # print(time_slots)
        quickReplyDTO=quickReply.getQuickReplyDTO(time_slots)
        obj = json.dumps(quickReplyDTO)
        a = json.loads(obj)
        print(a)
        return a


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
        # print(values)
        # result=text.getSimpleTextDTO(values)
        result='<p>This is Doctor '+doctor_name+' introduction:</p>'+'<p>'+values['information']+'</p>'
        obj = json.dumps(result)
        print(obj)
        return (json.loads(obj))

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

        html='<p>'+doctor_name+'<p>'
        html+= '<p>Information: '+information+'<p>'
        html+= '<p>Location: '+location+'<p>'
        html+= '<p>Specialization: '+specialization+'<p>'
        html+='<table class="table table-striped table-bordered table-hover table-condensed">'
        html+='<tr><th>start time</th><th>end time</th><th>book appointment</th></tr>'

        doctor_timetable=values['timetable']

        if doctor_timetable=='':
            result = dict()
            text = 'No available timeslot'
            result['data'] = text

            obj = json.dumps(result)
            b = (json.loads(obj))
            return b
        time_slots=timeslot.timetableToTimeSlot(doctor_timetable)
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


        # a=text.getTimeslotsTextDTO(result)
        obj = json.dumps(result)
        b=(json.loads(obj))
        return b




    def getAvailableDentists(self,conn):
        l=[]
        doctor_list=conn.find()
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
            for doctor in l:
                print(doctor)
                html += '<tr>'
                for key in doctor.keys():
                    html += '<td>' + doctor[key] + '</td>'
                html += '</tr>'
            html += '</table>'
            html += '</br>'
            html += "<p>You can enter 'doctor name + timeslot' to check the available timeslot (eg. James timeslot)</p>"
            doctorList['data'] = html
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






