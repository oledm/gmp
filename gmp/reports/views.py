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
    fake = {
        'investigationDate': '11.02.2016, 0:00:00',
        'measurers': [
            {'id': 5, 'name': 'Измеритель сопротивления, увлажненности и степени старения электроизоляции', 'verification': 'ПРВ-253156 от 02.04.2015', 'model': 'MIC-2500', 'department': 1, 'serial_number': '253156', 'expired_at': '2016-04-02'},
            {'id': 4, 'name': 'Измеритель сопротивления изоляции', 'verification': '0869567 от 23.04.2015', 'model': 'Metrel MI 3121H', 'department': 1, 'serial_number': '13341057', 'expired_at': '2016-04-23'}
        ],
        'lpu': 'Верхне-Казымское ЛПУ МГ',
        'team': [
            {'name': 'Алексеев Илья', 'rank': 'руководитель бригады'},
            {'name': 'Олейник Дмитрий', 'rank': 'член бригады'}
        ],
        'engine': {
            'type': 'ВАСО 16-14-24',
            'serial_number': '565465',
            'manufactured_at': '1986',
            'started_at': '1987',
        }
    }
    
    data = fake
    response = HttpResponse(content_type='application/pdf')
    report = Report(fake)
    report.make_report(response)
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    return response
