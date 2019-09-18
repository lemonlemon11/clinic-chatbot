def getListDTO(dataDict):
    # print(dataDict)
    data=dataDict['data']
    print(data)
    element_list=[]
    for value in data:
        d=dict()
        d['title']=value['timeslot']
        # d['image_url']="https://rockets.chatfuel.com/assets/shirt.jpg"
        d['subtitle']=value['doctor_name']+'\n'+value['timeslot']

        blocks_names=['cancel_appointment']
        title_lists=['Cancel']
        button_list=[]
        counter=0

        for name in blocks_names:
            inner_dict=dict()
            inner_dict['type']='show_block'
            attribute_dict=dict()
            attribute_dict['doctor_id']=value['doctor_id']+'_'+name
            attribute_dict['appointment_id']=value['appointment_id']
            attribute_dict['timeslot']=value['timeslot']

            inner_dict['set_attributes']=attribute_dict
            inner_dict['block_names']=[name]
            inner_dict['title']=title_lists[counter]
            counter+=1
            button_list.append(inner_dict)
        d['buttons']=button_list
        element_list.append(d)
    payload_dict=dict()
    payload_dict['template_type']='list'
    payload_dict['top_element_style']='compact'
    payload_dict['elements']=element_list

    attachment_dict=dict()
    attachment_dict['type']='template'
    attachment_dict['payload']=payload_dict

    message_dict=dict()
    message_dict['messages']=[{'attachment':attachment_dict}]
    return message_dict

