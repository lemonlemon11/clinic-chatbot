def getQuickReplyDTO(quickReplyDict):
    # print(quickReplyDict)
    if quickReplyDict==None:
        messages_dict=dict()
        quick_replies_list=[{'title':'Go back!','block_names':['Booking Options']}]
        messages_list=[{'text':'No available timeslot, please choose another doctor','quick_replies':quick_replies_list}]
        messages_dict['messages']=messages_list
        return messages_dict
    else:
        messages_dict=dict()
        quick_replies=[]
        for data in quickReplyDict:
            start_time=data['start_time']
            end_time=data['end_time']
            d=dict()
            d['title']=start_time+' - '+end_time
            d['block_names']=['Make Appointment']
            d['set_attributes']={'booking_time':start_time+' - '+end_time}
            quick_replies.append(d)
        messages_list=[{'text':'Appointment has been canceled, for','quick_replies':quick_replies}]
        messages_dict['messages']=messages_list
        return messages_dict

