import json

from django.http import HttpResponse

from .utils import Report

def create_report(request):
    #if request.method == "POST":
    fake = {
        'team': [{'rank': 'зам. руководителя бригады', 'name': 'Олейник Дмитрий'},
            {'rank': 'член бригады', 'name': 'Плахов Виталий'}
            ],
        'engine': {'type': 'ВАСО 16-14-24', 'serial_number': 'ff'}
    }
    #data = json.loads(request.body.decode('utf-8'))
    data = fake
    #print('Получены данные для формирования паспорта: ', data['report_data'])
    response = HttpResponse(content_type='application/pdf')
    report = Report(fake)
    #report.make_report(response, data['report_data'])
    report.make_report(response)
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    return response
