import json
import pprint

from django.http import HttpResponse

from .utils.reportmaker import ReportMaker

def create_report(request):
    #if request.method == "POST":
    data = json.loads(request.body.decode('utf-8'))
    print('\nПолучены данные для формирования паспорта\n')
    pprint.pprint(data['report_data'])
    response = HttpResponse(content_type='application/pdf')
    ReportMaker(data['report_data'], response)
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    return response

def create_report_debug(request):
    fake_passport = {'docs': [{'name': 'Журнал ремонта электродвигателя', 'value': True},
          {'name': 'Журнал эксплуатации электродвигателя', 'value': True},
          {'name': 'Инструкция по эксплуатации завода-изготовителя',
           'value': True},
          {'name': 'Протоколы штатных измерений и испытаний', 'value': True},
          {'name': 'Паспорт завода-изготовителя на взрывозащищенный '
                   'электродвигатель',
           'value': True},
          {'name': 'Схема электроснабжения электродвигателя', 'value': True}],
 'type': 'passport',
 'engine': {'manufactured_at': '1982-01-01T00:00:00.000Z',
            'new_date': '2026-08-27T00:00:00.000Z',
            'started_at': '1983-01-01T00:00:00.000Z',
            'serial_number': '5602',
            'station_number': '5А',
            'type': '2В100L6'},
 'files': {'main': '492', 'therm1': '602', 'therm2': '495'},
 'measurers': [4, 5, 6],
 'obj_data': {'ks': 'КС Ефремов',
              'location': 'АВО газа',
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
 'team': [{'name': 'Галкин Михаил Васильевич', 'rank': 'руководитель бригады'},
          {'name': 'Плахов Виталий Юрьевич ',
           'rank': 'зам. руководителя бригады',
           'required': False},
          {'name': 'Булавцев Константин Александрович',
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

    fake_report = {
 'type': 'report',
 'team': {'ЭЛ': 'Троянов Роман Васильевич',
         'ТК': 'Булавцев Константин Александрович',
         'УК': 'Галкин Михаил Васильевич',
         'ВД': 'Галкин Михаил Васильевич',
         'ВИК': 'Булавцев Константин Александрович'},
 'docs': ['Полис страхования риска ответственности за причинение вреда при эксплуатации опасного производственного объекта № 0100217262, серия 111 от 01.04.2015 г. на 1 л.',
          'Схема электроснабжения электродвигателя на 1 л.',
          'Журнал эксплуатации электродвигателя на 3 л.',
          'Приказ о закреплении оборудования за оперативно-ремонтным персоналом службы ЭТВС № 414 от 15.09.2014 г. на 6 л.',
          'Свидетельство о регистрации в государственном реестре опасных производственных объектов  АПО - 00174 от 21.11.2013 г. на 31 л.',
          'Лицензия на право эксплуатации взрывопожароопасных производственных объектов № ВП-00-009629 от 11.02.2009 г. на 32 л.',
          None,
          None],
  'files': {'licenses': ['15',
                        '16',
                        '18',
                        '19',
                        '17',
                        '21',
                        '20',
                        '22',
                        '23',
                        '24',
                        '25'],
           'main': ['11'],
           'therm1': ['12'],
           'therm2': ['13', '14']},
 'info': {'license': 'Договор № 321 от 13.04.2013 на выполнение работ по экспертизе промышленной безопасности.'},
 'engine': {'manufactured_at': '1982-01-01T00:00:00.000Z',
            'new_date': '2026-08-27T00:00:00.000Z',
            'started_at': '1983-01-01T00:00:00.000Z',
            'serial_number': '5602',
            'station_number': '5А',
            'type': '2В100L6'},
 "order": {"number":"ffdfs",
         "date":"2016-04-09T00:00:00.000Z"},
 'measurers': [4, 5, 6, 14, 20, 11, 13, 16],
 'obj_data': {'ks': 'КС Ефремов',
              'location': 'АВО газа',
              'lpu': 'Бобровское ЛПУ МГ',
              'org': 'ООО "Газпром трансгаз Югорск"',
              'plant': 'КЦ',
	      'detail_info': [
		  'Взрывозащищенный электродвигатель введен в '
		  'эксплуатацию в 1991 г.',
		  'Проектная и исполнительная документация на '
		  'монтаж взрывозащищенного электродвигателя '
		  'отсутствует.',
		  'Взрывозащищенный электродвигатель служит '
		  'приводом маслонасоса смазки агрегата №1 КЦ-2.',
		  'Взрывозащищенный электродвигатель '
		  'эксплуатируется как в автоматическом (без '
		  'присутствия постоянного обслуживающего '
		  'персонала), так и в ручном режиме.']
              },
 'resistance': {'isolation': '90',
                'wireAB': '65',
                'wireBC': '544',
                'wireCA': '6'},
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
 'workBegin': '2016-03-11T00:00:00.000Z',
 'workEnd': '2016-04-08T00:00:00.000Z',

 }

    fake_container_report = {
'device': {'carrier': 'Природный газ',
            'control': {'area': '100 % длины сварных соединений',
                        'name': 'УЗК'},
            'danger_class': 3,
            'dimensions_height_bottom': 127,
            'dimensions_height_ring': 1100,
            'dimensions_height_total': 2700,
            'dimensions_side_bottom': 20,
            'dimensions_side_ring': 20,
            'dimensions_width_bottom': 590,
            'dimensions_width_ring': 590,
            'factory': 'БМЗ 423200, г. Бугульма ТАССР',
            'full_desc': 'адсорбер зав.№ 2162, рег.№ 23051/А, инв.№ 100712',
            'full_desc_capital': 'Адсорбер зав.№ 2162, рег.№ 23051/А, инв.№ 100712',
            'id': 1,
            'inv_number': '100712',
            'location': 'Установка подготовки пускового, топливного и '
                        'импульсного газа',
            'manufactured_year': 1993,
            'material_bottom': 'Сталь марки 09Г2С ГОСТ 5520',
            'material_ring': 'Сталь марки 09Г2С ГОСТ 5520',
            'mode': 'Непрерывный без циклических нагрузок',
            'name': 'адсорбер',
            'p_test': 9.4,
            'p_work': 7.5,
            'reg_number': '23051/А',
            'scheme': 'БТ 2719.000.00-00.00 СБ',
            'serial_number': '2162',
            'started_year': 1996,
            'temp_carrier_high': 300,
            'temp_carrier_low': -20,
            'volume': 0.36,
            'weight': 1202,
            'welding': {'material': 'Сварочная проволока 08Г2С ГОСТ 2246-70',
                        'name': 'Электродуговая автоматическая'}},
 'obj_data': {'ks': 'КС "Кущевская"',
              'lpu': 'Ивдельское ЛПУ МГ',
              'org': 'ООО "Газпром трансгаз Югорск"',
              'plant': 'КЦ-1'},
 'type': 'report-container',
 'info': {'contract': '№ ГМП-16ДИА-0012',
          'license': 'Договор субподряда между ООО «ГАЗМАШПРОЕКТ» и ООО '
                     '«Стройгазмонтаж» № ГМП-16ДИА-0012 от 18.02.2016 г. '
                     '(договор между ООО «Газпром трансгаз Краснодар» и ООО '
                     '«Стройгазмонтаж» № 16ДИА-0012 от 18.02.2016 г.).'},
 'order': {'date': '2016-04-14T00:00:00.000Z', 'number': '№ 987654321/КЛМН'},

 }
    
    #data = fake_passport
    #data = fake_report
    data = fake_container_report
    response = HttpResponse(content_type='application/pdf')
    ReportMaker(data, response)
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    return response
