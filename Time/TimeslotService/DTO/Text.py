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