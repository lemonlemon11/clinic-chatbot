$(function () {
    $.backstretch("../static/assets/img/bg.jpg");
	var count = 0;
    var classes = [ "theme_1", "theme_2", "theme_3", "theme_4" ];
    var length = classes.length;
    $(function () {
        var timestamp = Date.parse(new Date());
        $("#user_id").val(timestamp)
        $('.pvr_chat_wrapper').toggleClass('active');
        $('.pvr_chat_button, .pvr_chat_wrapper .close_chat').on('click', function () {
            $('.pvr_chat_wrapper').toggleClass('active');
            return false;
        });

        $('.message-input').on('keypress', function (e) {
            if (e.which == 13) {
                var val = ($(this).val() !== '') ? $(this).val() : "Please type your message.";
                $('.chat-messages').append('<div class="message self"><div class="message-content">' + val + '</div></div>');
                var wixData;
                var intent='';
                var outputData;
                $.ajaxSettings.async=false
                $.ajax({
                    type: "get",
                    url: "https://api.wit.ai/message?v=20190327&q="+val,
                    headers: {
                        Authorization:'Bearer RBNF7TEFD3CEBH2MRIAM7KJQUVL7MWHO'
                    },
                    dataType: "json",
                    success: function(result){
                        console.log(result)
                        var keys1 = [];
                        for (var p1 in result['entities']) {
                            if (result['entities'].hasOwnProperty(p1))
                                keys1.push(p1);
                        }
                        if(keys1=='') {
                            intent='';
                            $("#intent").val(intent)
                        }
                        else {
                            intent=result['entities']['intent'][0]['value']
                            $("#intent").val(intent)
                            wixData=result
                        }
                    }
                });

                var url;
                intent_value=$("#intent").val()

                if(intent_value=='greeting'){
                    outputData = wixData['entities']['greeting'][0]['value']
                    url="http://127.0.0.1:7777/Doctors/"+intent_value+'/'+outputData

                }
                if(intent_value==''){
                    msg_option='Sorry, Dentist Chatbot can not understand your question.</br></br>'
                    msg_option+='These are the questions for asking the "Dentist Chatbot"'
                    msg_option+='<ul>'
                    msg_option+='<li>show dentist list</li>'
                    msg_option+='<li>list available dentists</li>'
                    msg_option+='<li>check my appointments</li>'
                    msg_option+='<li>list available timeslot of + (doctor name)</li>'
                    msg_option+='<li>(doctor name) + information</li>'
                    msg_option+='</ul>'
                    setTimeout(function () {
                            $('.chat-messages').append('<div class="message"><div class="message-content">' + msg_option + '</div></div>');
                        $messages_w.scrollTop($messages_w.prop("scrollHeight"));
                        $messages_w.perfectScrollbar('update');
                    }, 200)
                }
                if (intent_value=='checkAppointment'){
                    user_id=$("#user_id").val()
                    doctor_name=$("#doctor_name").val()
                    url="http://127.0.0.1:9999/Timeslots/"+intent_value+"/"+user_id

                }
                if (intent_value=='getAllDoctors'){
                    url="http://127.0.0.1:7777/Doctors/"+intent_value
                }
                if (intent_value=='getAvailableDentist'){
                    url="http://127.0.0.1:7777/Doctors/"+intent_value
                }
                if(intent_value=='getDentistInformationByName') {
                    var k = [];
                    for (var p1 in wixData['entities']) {
                        if (wixData['entities'].hasOwnProperty(p1))
                            k.push(p1);
                    }
                    if(k.indexOf('people_name')!=-1){
                        outputData = wixData['entities']['people_name'][0]['value']
                        url="http://127.0.0.1:7777/Doctors/"+intent_value+'/'+outputData
                    }else {
                        msg_1='Dotor does not exist, please type "show dentist list" to check doctors'
                        setTimeout(function () {
                            $('.chat-messages').append('<div class="message"><div class="message-content">' + msg_1 + '</div></div>');
                            $messages_w.scrollTop($messages_w.prop("scrollHeight"));
                            $messages_w.perfectScrollbar('update');
                        }, 200)
                    }
                }
                if (intent_value=='getAvailableTimeslotByName'){
                    var k = [];
                    for (var p1 in wixData['entities']) {
                        if (wixData['entities'].hasOwnProperty(p1))
                            k.push(p1);
                    }
                    if(k.indexOf('people_name')!=-1){
                    // console.log(wixData)
                        outputData = wixData['entities']['people_name'][0]['value']
                        url="http://127.0.0.1:7777/Doctors/"+intent_value+'/'+outputData
                    }else {
                        msg_1='Dotor does not exist, please type "show dentist list" to check doctors'
                        setTimeout(function () {
                            $('.chat-messages').append('<div class="message"><div class="message-content">' + msg_1 + '</div></div>');
                            $messages_w.scrollTop($messages_w.prop("scrollHeight"));
                            $messages_w.perfectScrollbar('update');
                        }, 200)
                    }
                }
                if (intent_value!=''){
                    $.ajax({
                        type: "get",
                        url: url,
                        // data:{data:outputData},
                        dataType: "json",
                        success: function(result){
                            console.log(result)
                            setTimeout(function () {
                                $('.chat-messages').append('<div class="message"><div class="message-content">' + result['data'] + '</div></div>');
                                $messages_w.scrollTop($messages_w.prop("scrollHeight"));
                                $messages_w.perfectScrollbar('update');
                            }, 200)
                        }
                    });
                }
                $(this).val('');
                var $messages_w = $('.pvr_chat_wrapper .chat-messages');
                $messages_w.scrollTop($messages_w.prop("scrollHeight"));
                $messages_w.perfectScrollbar('update');
                return false;
            }
        });

        $('.pvr_chat_wrapper .chat-messages').perfectScrollbar();
        $(".change_chat_theme").on('click', function () {
            $(".chat-messages").removeAttr("class").addClass("chat-messages " + classes[ count ]);
            if (parseInt(count, 10) === parseInt(length, 10) - 1) {
                count = 0;
            } else {
                count = parseInt(count, 10) + 1;
            }
            var $messages_w = $('.pvr_chat_wrapper .chat-messages');
            $messages_w.scrollTop($messages_w.prop("scrollHeight"));
            $messages_w.perfectScrollbar('update');
        })
    });
});

function f1(appointment_id,appointment_time,doctor_id) {
    url="http://127.0.0.1:5002/Timeslots/cancelAppointmentByAppointmentID"
    // url="http://127.0.0.1:5000/Timeslots/cancelAppointmentByAppointmentID"
    var data= {
                'appointment_id': appointment_id,
                'appointment_time': appointment_time,
                'doctor_id': doctor_id,
            }
    $.ajax({
        type: "post",
        url: url,
        data: data,
        dataType: "json",
        success: function(result){
            console.log(result)
            msg=result['data']
            setTimeout(function () {
                $('.chat-messages').append('<div class="message"><div class="message-content">' + result['data'] + '</div></div>');
                $messages_w.scrollTop($messages_w.prop("scrollHeight"));
                $messages_w.perfectScrollbar('update');
            }, 200)
        }
    });
    $(this).val('');
    var $messages_w = $('.pvr_chat_wrapper .chat-messages');
    $messages_w.scrollTop($messages_w.prop("scrollHeight"));
    $messages_w.perfectScrollbar('update');
    return false;
}

function f(appointment_time,location,doctor_id,doctor_name) {
    user_id=$("#user_id").val()
    // alert(user_id)
    // doctor_id=$("#doctor_id").val()
    // doctor_name=$("#doctor_name").val()
    // alert(doctor_name)
    // alert(doctor_id)
    url="http://127.0.0.1:5002/Timeslots/bookAppointment"
    var data= {
            'doctor_id': doctor_id,
            'appointment_time': appointment_time,
            'location': location,
            'user_id':user_id,
            'doctor_name':doctor_name
            }
    $.ajax({
        type: "post",
        url: url,
        data: data,
        dataType: "json",
        success: function(result){
            console.log(result)
            msg=result['data']
            setTimeout(function () {
                $('.chat-messages').append('<div class="message"><div class="message-content">' + result['data'] + '</div></div>');
                $messages_w.scrollTop($messages_w.prop("scrollHeight"));
                $messages_w.perfectScrollbar('update');
            }, 200)
        }
    });
    $(this).val('');
    var $messages_w = $('.pvr_chat_wrapper .chat-messages');
    $messages_w.scrollTop($messages_w.prop("scrollHeight"));
    $messages_w.perfectScrollbar('update');
    return false;
}