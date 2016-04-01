from .passport import Passport
from .report import Report

class ReportMaker():
    def __init__(self, data, report):
        if data['type'] == 'passport':
            Passport(data, report, 'Паспорт двигателя ' + data['engine']['type'])
        if data['type'] == 'report':
            Report(data, report, 'Заключение экспертизы двигателя ' + data['engine']['type'])
