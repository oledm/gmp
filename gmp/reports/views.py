import json

from django.http import HttpResponse

from .utils import Report

def create_report(request):
    #if request.method == "POST":
    data = json.loads(request.body.decode('utf-8'))
    print('Получены данные для формирования паспорта: ', data['report_data'])
    response = HttpResponse(content_type='application/pdf')
    report = Report()
    report.make_report(response, data['report_data'])
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    return response
