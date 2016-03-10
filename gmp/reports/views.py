import json

from django.http import HttpResponse

from .utils import Report

def create_report(request):
    #if request.method == "POST":
    data = json.loads(request.body.decode('utf-8'))
    print('Получены данные для формирования паспорта: ', data['report_data'])
    response = HttpResponse(content_type='application/pdf')
    report = Report(data['report_data'])
    report.make_report(response)
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    return response

def create_report_debug(request):
    fake = {'measurers': [{'verification': '0869567 от 23.04.2015', 'serial_number': '13341057', 'id': 4, 'department': 1, 'name': 'Измеритель сопротивления изоляции', 'model': 'Metrel MI 3121H', 'expired_at': '2016-04-23'}, {'verification': 'ПРВ-253156 от 02.04.2015', 'serial_number': '253156', 'id': 5, 'department': 1, 'name': 'Измеритель сопротивления, увлажненности и степени старения электроизоляции', 'model': 'MIC-2500', 'expired_at': '2016-04-02'}, {'verification': '15-059 от 15.04.2015', 'serial_number': '1634/4086', 'id': 6, 'department': 1, 'name': 'Прибор для измерения и анализа вибрации', 'model': 'Агат-М', 'expired_at': '2016-04-15'}], 'ks': 'КС Майкоп', 'workEnd': '05.03.2016, 0:00:00', 'investigationDate': '02.03.2016, 0:00:00', 'workBegin': '01.03.2016, 0:00:00', 'lpu': 'Алмазное ЛПУ МГ', 'docs': [{'value': True, 'name': 'Журнал ремонта электродвигателя'}, {'value': True, 'name': 'Журнал эксплуатации электродвигателя'}, {'value': True, 'name': 'Инструкция по эксплуатации завода-изготовителя'}, {'value': True, 'name': 'Протоколы штатных измерений и испытаний'}, {'value': True, 'name': 'Паспорт завода-изготовителя на взрывозащищенный электродвигатель'}, {'value': True, 'name': 'Схема электроснабжения электродвигателя'}], 'plant': 'Цех сжатия', 'org': 'ООО "Газпром трансгаз Чайковский"', 'engine': {'type': 'ВАСО 16-14-24', 'manufactured_at': '1987', 'serial_number': '345454', 'station_number': '1-15', 'started_at': '1988', 'location': 'АВО газа'}, 'team': [{'rank': 'член бригады', 'name': 'Алексеев Илья'}]}
    
    data = fake
    response = HttpResponse(content_type='application/pdf')
    report = Report(fake)
    report.make_report(response)
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    return response
