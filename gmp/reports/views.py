from django.shortcuts import render
from django.http import HttpResponse

from .utils import make_report

def create_report(request):
    make_report()
    return HttpResponse('Report is creating')
