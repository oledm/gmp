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
 'engine': {'manufactured_at': '1982-01-01T00:00:00.000Z',
            'new_date': '2026-08-27T00:00:00.000Z',
            'started_at': '1983-01-01T00:00:00.000Z',
            'serial_number': '5602',
            'station_number': '5А',
            'type': '2В100L6'},
 'files': {'main': '492', 'therm1': '494', 'therm2': '495'},
 'measurers': [4, 5, 6],
 'obj_data': {'ks': 'КС Ефремов',
              'location': '5',
              'lpu': 'Бобровское ЛПУ МГ',
              'org': 'ООО "Газпром трансгаз Югорск"',
              'plant': 'КЦ'},
 'resistance': {'isolation': '90',
                'wireAB': '65',
                'wireBC': '544',
                'wireCA': '6'},
 'signers': {'approve': {'fio': 'В.И. Давлетов',
                         'rank': 'Главный инженер филиала ООО "Газпром '
                                 'трансгаз Москва" Тульское ЛПУ МГ'},
             'signer': {'fio': 'Л.А. Политов',
                        'rank': 'Заместитель начальника службы ЭТВС филиала '
                                'ООО "Газпром трансгаз Москва" Тульское ЛПУ '
                                'МГ'}},
 'team': [{'name': 'Алексеев Илья Сергеевич', 'rank': 'руководитель бригады'},
          {'name': 'Плахов Виталий Юрьевич',
           'rank': 'зам. руководителя бригады',
           'required': False},
          {'name': 'Олейник Дмитрий Алексеевич',
           'rank': 'член бригады',
           'required': False}],
 'therm': {'correct': 'Соответствует',
           'distance': '2',
           'tclass': 2,
           'temp_avg': '36,3',
           'temp_env': '20',
           'temp_max': '19',
           'temp_min': '56'},
 'values': {'factory_values': {'resistance_isolation': '1,2',
                               'resistance_phase': '323,21'}},
 'vibro': {'axis': '67',
           'horiz': '6789',
           'norm': '45',
           'reverse_axis': '56',
           'reverse_horiz': '678',
           'reverse_vert': '7896',
           'vert': '789'},
 'investigationDate': '2016-03-18T00:00:00.000Z',
 'workBegin': '2016-03-11T00:00:00.000Z',
 'workEnd': '2016-04-08T00:00:00.000Z'}




    
    data = fake
    response = HttpResponse(content_type='application/pdf')
    report = Report(fake)
    report.make_report(response)
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    return response
