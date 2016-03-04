from django.http import HttpResponse

from .utils import make_report

def create_report(request):
    print('REQUEST', request.POST)
    response = HttpResponse(content_type='application/pdf')
    make_report(response)
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    return response
