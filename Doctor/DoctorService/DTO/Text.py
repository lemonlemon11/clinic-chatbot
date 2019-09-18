# {
#  "messages": [
#    {"text": "Welcome to the Chatfuel Rockets!",
#    "set_attributes": {"doctor_id":"xxx"}
#    },
#    {"text": "What are you up to?"}
#  ]
# }


def getSimpleTextDTO(textDict):
    textList=textDict['information']

    l=[]
    d=dict()
    d['text']=textList
    l.append(d)
    print(l)
    return {'messages':l}

def getTimeslotsTextDTO(textDict):
    data=(textDict['data'])
    timetables=data['timetable']
    print('timetables',timetables)
    if timetables==None:
        return {"messages": [{"text": "We are sorry about that"}]}
    else:
        msg=''
        for timetable in timetables:
            start_time=timetable['start_time']
            end_time=timetable['end_time']
            msg+='From '+start_time+' to '+end_time+'\n'
        l=[]
        set_attributes=dict()
        set_attributes['doctor_id']=data['doctor_id']
        set_attributes['doctor_name']=data['doctor_name']
        l.append({'text':msg,'set_attributes':set_attributes})
        return {'messages':l}