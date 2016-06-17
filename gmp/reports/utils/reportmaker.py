from .passport import Passport
from .report import Report
from .report_container import ReportContainer

from gmp.containers.models import ContainerType

def upperFirstLetter(word):
    return word[0].upper() + word[1:]

class ReportMaker():
    def __init__(self, data, report):
        if data['type'] == 'passport':
            Passport(data, report, 'Паспорт двигателя ' + data['engine']['type'])
        if data['type'] == 'report':
            Report(data, report, 'Заключение экспертизы двигателя ' + data['engine']['type'])
        if data['type'] == 'report-container':
            container_type = ContainerType.objects.get(pk=data['device']['_type'])
            desc = '{} зав.№ {}, рег.№ {}, инв.№ {}'.format(
                container_type,
                data['obj_data']['serial_number'],
                data['obj_data']['reg_number'],
                data['obj_data']['inv_number'],
            )
            data['device'].update({
                'full_desc': desc,
                'full_desc_capital': upperFirstLetter(desc),
                'serial_number': data['obj_data']['serial_number'],
                'reg_number': data['obj_data']['reg_number'],
                'inv_number': data['obj_data']['inv_number'],
                'scheme': data['obj_data']['scheme'],
                'manufactured_year': data['obj_data']['manufactured_year'],
                'started_year': data['obj_data']['started_year'],
                'location': data['obj_data']['location'],

            })
            ReportContainer(data, report, data['device']['full_desc_capital'])
