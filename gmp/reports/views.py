import json
import pprint

from django.http import HttpResponse

from .utils import Report

def create_report(request):
    #if request.method == "POST":
    data = json.loads(request.body.decode('utf-8'))
    print('\nПолучены данные для формирования паспорта\n')
    pprint.pprint(data['report_data'])
    response = HttpResponse(content_type='application/pdf')
    report = Report(data['report_data'])
    report.make_report(response)
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    return response

def create_report_debug(request):
    fake = {'docs': [{'name': 'Журнал ремонта электродвигателя', 'value': True},
          {'name': 'Журнал эксплуатации электродвигателя', 'value': True},
          {'name': 'Инструкция по эксплуатации завода-изготовителя',
           'value': True},
          {'name': 'Протоколы штатных измерений и испытаний', 'value': True},
          {'name': 'Паспорт завода-изготовителя на взрывозащищенный '
                   'электродвигатель',
           'value': True},
          {'name': 'Схема электроснабжения электродвигателя', 'value': True}],
 'engine': {'manufactured_at': '1987',
            'serial_number': '5602',
            'started_at': '1989',
            'station_number': '5А',
            'type': 'ВАСО 16-14-24'},
 'investigationDate': '02.03.2016, 0:00:00',
 'measurers': [{'department': 1,
                'expired_at': '2016-04-23',
                'id': 4,
                'model': 'Metrel MI 3121H',
                'name': 'Измеритель сопротивления изоляции',
                'serial_number': '13341057',
                'verification': '0869567 от 23.04.2015'},
               {'department': 1,
                'expired_at': '2016-04-02',
                'id': 5,
                'model': 'MIC-2500',
                'name': 'Измеритель сопротивления, увлажненности и степени '
                        'старения электроизоляции',
                'serial_number': '253156',
                'verification': 'ПРВ-253156 от 02.04.2015'},
               {'department': 1,
                'expired_at': '2016-04-15',
                'id': 6,
                'model': 'Агат-М',
                'name': 'Прибор для измерения и анализа вибрации',
                'serial_number': '1634/4086',
                'verification': '15-059 от 15.04.2015'}],
 'obj_data': {'ks': 'КС Ефремов',
              'location': 'АВО газа',
              'lpu': 'Бардымское ЛПУ МГ',
              'org': 'ООО "Газпром трансгаз Чайковский"',
              'plant': 'КЦ'},
 'team': [{'name': 'Плахов Виталий', 'rank': 'руководитель бригады'},
          {'name': 'Алексеев Илья', 'rank': 'член бригады'}],
 'workBegin': '01.03.2016, 0:00:00',
 'workEnd': '05.03.2016, 0:00:00'}


    
    data = fake
    response = HttpResponse(content_type='application/pdf')
    report = Report(fake)
    report.make_report(response)
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    return response
