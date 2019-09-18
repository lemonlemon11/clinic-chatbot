import requests
import DoctorService.Services.DoctorServices as doctorService
import DoctorService.Utils.DBConnection as conn
expression='all doctors'
result=requests.get('https://api.wit.ai/message?v=20190326&q={}'.format(expression),headers={'Authorization':'Bearer C6V3NVVPSAXPDF23CGK2H4MYAKQ5C7FE'})
jsonResult=result.json()
print(jsonResult)
if jsonResult['entities']['intent'][0]['value']=='GetAllDoctors':
    obj=doctorService.DoctorServices()
    print(obj.getAllDoctor(conn.getDBConnection()))