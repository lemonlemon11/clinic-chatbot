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
# s='9'
# print(timetableToTimeSlot(s))

