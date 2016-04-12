from .passport import Passport
from .report import Report
from .report_container import ReportContainer

class ReportMaker():
    def __init__(self, data, report):
        if data['type'] == 'passport':
            Passport(data, report, 'Паспорт двигателя ' + data['engine']['type'])
        if data['type'] == 'report':
            Report(data, report, 'Заключение экспертизы двигателя ' + data['engine']['type'])
        if data['type'] == 'report-container':
            ReportContainer(data, report, data['device']['full_desc_capital'])
