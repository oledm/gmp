from functools import partial
from datetime import datetime
from json import dumps

from reportlab.platypus import Paragraph, Spacer, Image, Table, TableStyle, PageBreak, NextPageTemplate
from reportlab.lib.styles import ParagraphStyle as PS
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.platypus.frames import Frame
from reportlab.platypus.doctemplate import PageTemplate
from reportlab.lib.units import cm
from reportlab.lib import colors

from gmp.authentication.models import Employee
from gmp.certificate.models import Certificate, EBcertificate
#from gmp.inspections.models import Organization, LPU
from gmp.departments.models import Measurer
from gmp.engines.models import Engine, ThermClass, Connection
from gmp.filestorage.models import FileStorage

from .helpers import ReportMixin, DoubledLine
from .excel_import import ExcelImporter


class Passport(ReportMixin):
    def __init__(self, data, report, title):
        toc_styles = ('TOCHeading3', 'TOCHeading3')
        super().__init__(data, report, title, leftMargin=1.2, rightMargin=.5, toc_styles=toc_styles)

    def create(self):
        self.procExcelData()
        self.setup_page_templates(self.doc)

        # Filter empty team members appeared after accident click on 'Add'
        # team's member button
        self.data['team'] = list(filter(lambda x: x.get('id') and x.get('rank'), self.data['team']))

        if not self.data['files'].get('excel'):
            self.format_JS_dates(self.data['engine'], ('manufactured_at', 'started_at'), '%Y')
            self.format_JS_dates(self.data['engine'], ('new_date',))
            self.format_JS_dates(self.data, ('workBegin', 'workEnd', 'investigationDate'))

        self.connection = Connection.objects.get(pk=self.data['engine']['connection'])

        self.Story.append(NextPageTemplate('Title'))
        self.page1()
        self.put_toc()
        self.toc_entry = [
            {
                'width': 0.25,
                'font':  {
                    'name': 'Regular',
                    'fontName': 'Times',
                    'fontSize': 13,
                    'leading': 14,
                    'alignment': TA_LEFT
                }
            },
            {
                'width': 0.75,
                'font':  {
                    'name': 'Regular',
                    'fontName': 'Times',
                    'fontSize': 13,
                    'leading': 14,
                    'alignment': TA_LEFT
                }
            }

        ]
        self.Story.append(NextPageTemplate('Content'))
        self.page3()
        self.page4()
        self.page5_6()
        self.page7()
        self.page8()
        self.page9()
        self.page10()
        self.page11()
        self.page12()
        self.page13()
        self.page14()
        self.page15()
        self.page16()
        self.page17()
        self.page18()
        self.page19()
        self.page20()
        self.page21()
        self.appendix('1 Сведения об эксплуатации электродвигателя',
            ['Дата', 'Число пусков', 'Суммарная наработка, час'],
            [2, 3, 5])
        self.appendix('2 Сведения об испытаниях электродвигателя',
            ['Дата', 'Вид', 'Содержание', 'Заключение'],
            [1, 2, 3, 4])
        self.appendix('3 Сведения о ремонтах электродвигателя',
            ['Дата', 'Вид', 'Содержание', 'Заключение'],
            [1, 2, 3, 4])

    def procExcelData(self):
        try:
            file_entry = FileStorage.objects.get(pk=int(self.data['files']['excel'][0]['id']))
        except IndexError:
            return
        file_ = self.get_file(file_entry.fileupload)
        excel_importer = ExcelImporter()
        header, rows = excel_importer.read(file_)
        rows_w_values = dict(map(lambda x: (x[0], x[1]), filter(lambda x: x[1], rows)))

        self.data['obj_data']['ks'] = rows_w_values['Наименование КС или установки']
        self.data['obj_data']['plant'] = rows_w_values['Название цеха']
        self.data['obj_data']['location'] = rows_w_values['Место установки']

        self.data['engine']['serial_number'] = rows_w_values['Заводской номер']
        self.data['engine']['station_number'] = rows_w_values['Станционный номер']
        self.data['engine']['manufactured_at'] = rows_w_values['Год изготовления']
        self.data['engine']['started_at'] = rows_w_values['Год ввода в эксплуатацию']
        self.data['engine']['new_date'] = rows_w_values['Дата продления срока эксплуатации']

        self.data['workBegin'] = rows_w_values['Дата начала работ']
        self.data['investigationDate'] = rows_w_values['Дата обследования']
        self.data['workEnd'] = rows_w_values['Дата окончания работ']

        if 'values' not in self.data:
            self.data.update(values={'factory_values': {}})
        self.data['values']['factory_values']['resistance_isolation'] = rows_w_values['Сопротивление изоляции обмотки статора относительно корпуса двигателя, МОм']
        self.data['values']['factory_values']['resistance_phase'] = rows_w_values['Сопротивление фазы обмотки статора постоянному току в холодном состоянии при 20°C']

        self.data['therm']['distance'] = rows_w_values['Расстояние до объекта, м']
        self.data['therm']['temp_env'] = rows_w_values['Температура окружающей среды']
        self.data['therm']['temp_max'] = rows_w_values['Максимальная температура, °С']
        self.data['therm']['temp_min'] = rows_w_values['Минимальная температура, °С']
        self.data['therm']['temp_avg'] = rows_w_values['Средняя температура, °С']

        self.data['vibro']['vert'] = rows_w_values['Подшипниковый узел со стороны привода (вертикальная зона)']
        self.data['vibro']['horiz'] = rows_w_values['Подшипниковый узел со стороны привода (горизонтальная зона)']
        self.data['vibro']['axis'] = rows_w_values['Подшипниковый узел со стороны привода (осевая зона)']
        self.data['vibro']['reverse_vert'] = rows_w_values['Подшипниковый узел с противоположной приводу (вертикальная зона)']
        self.data['vibro']['reverse_horiz'] = rows_w_values['Подшипниковый узел с противоположной приводу (горизонтальная зона)']
        self.data['vibro']['reverse_axis'] = rows_w_values['Подшипниковый узел с противоположной приводу (осевая зона)']
        self.data['vibro']['norm'] = rows_w_values['Норма']

        self.data['resistance']['isolation'] = rows_w_values['Сопротивление изоляции, МОм']
        self.data['resistance']['wireAB'] = rows_w_values['Сопротивление обмотки, мОм (фаза A-B)']
        self.data['resistance']['wireBC'] = rows_w_values['Сопротивление обмотки, мОм (фаза B-C)']
        self.data['resistance']['wireCA'] = rows_w_values['Сопротивление обмотки, мОм (фаза C-A)']

        if 'signers' not in self.data:
            self.data.update(signers={'approve': {}, 'signer': {}})
        self.data['signers']['approve']['rank'] = rows_w_values['Кто утверждает (должность)']
        self.data['signers']['approve']['fio'] = rows_w_values['Кто утверждает (ФИО)']
        self.data['signers']['signer']['rank'] = rows_w_values['Подписант из службы (должность)']
        self.data['signers']['signer']['fio'] = rows_w_values['Подписант из службы (ФИО)']

    def put_toc(self):
        self.new_page()
        self.put('Содержание', 'Regular Bold Center', 0.5)
        self.Story.append(self.toc)

    def add_to_toc(self, *entries):
        toc_entry = []
        for num, item in enumerate(self.toc_entry):
            toc_entry.append({ **item, 'text': entries[num]})
        json_toc_entry = dumps(toc_entry)
        super().add_to_toc(json_toc_entry, self.styles['TOC Hidden'])

    def page1(self):
        self.put('ПАО "ГАЗПРОМ"', 'Heading 1 Bold')
        self.Story.append(DoubledLine(self.full_width))
        self.put('РОССИЙСКАЯ ФЕДЕРАЦИЯ<br/>ООО «ГАЗМАШПРОЕКТ»', 'Heading 1 Bold')

        self.Story.append(Spacer(1, 0.5 * cm))

        signers = self.data['signers']['approve']
        date_string = '"___"{:_>20}'.format('_') + '{} г.'.format(datetime.now().year)
        fio_string = '{fio:_>30}'
        first_col = ['"Согласовано"', '{rank}', fio_string,
             date_string    
        ]
        second_col = [
            '"Утверждаю"',
            'Директор филиала<br/>ООО «ГАЗМАШПРОЕКТ» «НАГАТИНСКИЙ»',
            fio_string.format(fio='Р.Ю. Ерин'),
            date_string    
        ]
        template = list(zip(first_col, ['&nbsp;'] * len(first_col), second_col))
        cols = len(template[0])
        styles = [
            ['Heading 1 Bold'] * cols,
            ['Heading 1'] * cols,
            *[['Regular'] * cols] * 2,
        ]
        table_data = self.values(template, signers)
        table = self.table(table_data, styles, [4.3, 1.4, 4.3], styleTable=False)
        table.hAlign = 'LEFT'
        table.setStyle(TableStyle([
            ('BOTTOMPADDING', (0,0), (-1,-1), 15),
            ('BOTTOMPADDING', (0,0), (-1,0), 20),
            ('BOTTOMPADDING', (0,1), (-1,1), 20),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ]))
        self.Story.append(table)
        self.Story.append(Spacer(1, 1.0 * cm))

        self.mput([
            'ПАСПОРТ 1-2/1715-10-14',
            'ТЕХНИЧЕСКОГО СОСТОЯНИЯ',
            'ВЗРЫВОЗАЩИЩЁННОГО ЭЛЕКТРОДВИГАТЕЛЯ',
        ], 'MainTitle', 1)

        text = '''ОБЪЕКТ: {org[name]}<br/>{lpu[name]}<br/>{ks}<br/>{plant}<br/>{location}<br/>
            станционный № {station_number}<br/>
            ТИП: {type} зав.№ {serial_number}'''.format(
                **self.data['obj_data'], **self.data.get('engine')
        )
        self.put(text, 'MainTitle', 1)
        self.put('Дата обследования: ' + self.data['investigationDate'], 'Heading 1', 2)

        signers = self.data['signers']['signer']
        first_col = ['{rank}', fio_string, date_string]
        second_col = [
            'Начальник проектно-<br/>диагностического отдела<br/>ООО «ГАЗМАШПРОЕКТ»<br/>«НАГАТИНСКИЙ»',
            fio_string.format(fio='И.Ю. Медведев'),
            date_string    
        ]
        template = list(zip(first_col, ['&nbsp;'] * len(first_col), second_col))
        cols = len(template[0])
        styles = [
            ['Heading 1'] * cols,
            *[['Regular'] * cols] * 2,
        ]
        table_data = self.values(template, signers)
        table = self.table(table_data, styles, [4.3, 1.4, 4.3], styleTable=False)
        table.hAlign = 'LEFT'
        table.setStyle(TableStyle([
            ('BOTTOMPADDING', (0,0), (-1,-1), 15),
            ('BOTTOMPADDING', (0,1), (-1,1), 20),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ]))
        self.Story.append(table)

    def page3(self):
        self.Story.append(PageBreak())
        self.add_to_toc('ФОРМУЛЯР № 1', 'Регистрация работ')
        self.formular('1 Регистрация работ')

        ptext = '<b>Фамилия И.О.</b><br/>' + '<br/>'.join(
                [Employee.objects.get(pk=x['id']).fio() for x in self.data.get('team')]
        )
        left = Paragraph(ptext, self.styles['Table Content']) 
        ptext = '<b>Должность</b><br/>' + '<br/>'.join(
                [x.get('rank', '') for x in self.data.get('team')]
        )
        right = Paragraph(ptext, self.styles['Table Content']) 
        team_table = Table([[left, right]])
        team_table.hAlign = 'LEFT'
        style = TableStyle([
            ('FONTNAME', (0,0), (-1,-1), 'Times'),
            ('FONTSIZE', (0,0), (-1,-1), 13),
            ('TOPPADDING', (0,0), (-1,-1), 12),
            ('BOTTOMPADDING', (0,0), (-1,-1), 12),
            ('LEADING', (0,0), (-1,-1), 16),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ])
        team_table.setStyle(style)

        text = '<br />'.join(['____________________' + Employee.objects.get(pk=x['id']).fio() for x in self.data.get('team')])
        table2 = Table([[Paragraph(text, self.styles['Signature Left'])]])
        table2.hAlign = 'LEFT'
        table2.setStyle(style)

        table_data = [
            ['ВИД РАБОТ', 'Техническое диагностирование'],
            ['ДАТА НАЧАЛА', self.data['workBegin']],
            ['ДАТА ОКОНЧАНИЯ', self.data['workEnd']],
            [Paragraph('СОСТАВ БРИГАДЫ СПЕЦИАЛИСТОВ', self.styles['Regular Bold Center']), team_table],
            ['ОРГАНИЗАЦИЯ', 'ООО "ГАЗМАШПРОЕКТ"'],
            ['РАЗРЕШЕНИЕ', '''Свидетельство об аккредитации 766-Э/ТД выдано Управлением\nэнергетики ОАО "Газпром" 11 февраля 2015 г.\nСрок действия до 11 февраля 2018 г.'''],
            ['СУБПОДРЯДНАЯ\nОРГАНИЗАЦИЯ', ''],
            ['РАЗРЕШЕНИЕ\nСУБПОДРЯДНОЙ\nОРГАНИЗАЦИИ', ''],
            ['ПОДПИСИ\nЧЛЕНОВ\nБРИГАДЫ', table2],
        ]

        table = Table(table_data, colWidths=self.columnize(3,7))
        table.hAlign = 'LEFT'
        table.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), 'Times'),
            ('FONTSIZE', (0,0), (-1,-1), 13),
            ('TOPPADDING', (0,0), (-1,-1), 12),
            ('BOTTOMPADDING', (0,0), (-1,-1), 12),
            ('LEADING', (0,0), (-1,-1), 16),
            ('BOX', (0,0), (-1,-1), 0.5, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (0,-1), 'Times Bold'),
            ('LINEABOVE', (0,1), (-1,1), 0.5, colors.black),
            ('LINEABOVE', (0,3), (-1,-1), 0.5, colors.black),
            ('BOX', (0,0), (0,-1), 0.5, colors.black),
        ]))
        self.Story.append(table)
        #self.Story.append(Spacer(1, 1 * cm))

    def page4(self):
        self.Story.append(PageBreak())
        # Table header
        template = [
            ['Список сертифицированных членов бригады', *['']*7],
            [
                '№ п/п', 'Фамилия И.О.', '№ квалифика-<br/>ционного удостоверения',
                'Дата выдачи', 'Срок дейст-<br/>вия', 'Виды конт-<br/>роля', 'Уро-<br/>вень', 'Группа ЭБ'
            ]
        ]
        table_data = self.values(template, {})
        cols = len(table_data[0])
        styles = [
            *[['Regular Bold Center']],
            *[['Regular Center'] * cols],
        ]
        table = self.table(table_data, styles, [1, 2, 2, 1, 1, 1, 1, 1], styleTable=True)
        table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('SPAN', (0, 0), (-1, 0)),
            ('BOTTOMPADDING', (0,0), (-1,-1), 12),
            ('TOPPADDING', (0,0), (-1,-1), 7),
        ]))
        self.Story.append(table)

        # For each person generate separate table for ability to span 
        # certain fields
        for num, person in enumerate(self.data.get('team'), start=1):
            emp = Employee.objects.get(pk=person['id'])
            try:
                eb_cert = emp.ebcertificate.get_group_display()
            except EBcertificate.DoesNotExist:
                eb_cert = 'Нет данных'
            cert = Certificate.objects.filter(employee=emp)
            all_cert = [
                [str(num), emp.fio()] +
                c.plain_details('<br />') +
                [eb_cert] 
                for c in cert
            ] or [
                [str(num), emp.fio(), *['Нет данных'] * 5, eb_cert]
            ]
            table_data = self.values(all_cert, {})
            cols = len(table_data[0])
            rows = len(table_data)
            styles = [
                *[['Regular Center'] * cols] * rows,
            ]
            table = self.table(table_data, styles, [1, 2, 2, 1, 1, 1, 1, 1], styleTable=False)
            table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('SPAN', (0,0), (0, rows - 1)),
                ('SPAN', (1,0), (1, rows - 1)),
                ('SPAN', (7,0), (7, rows - 1)),
                # No padding between in-table rows
                ('BOTTOMPADDING', (0,0), (-1,-1), 0),
                ('TOPPADDING', (0,0), (-1,-1), 0),
                # Add padding for the first and last table's rows
                ('BOTTOMPADDING', (0,-1), (-1,-1), 4),
                ('TOPPADDING', (0,0), (-1,0), 4),
                ('LINEAFTER',(0,0),(-1,-1), 0.5, colors.black),
                ('BOX', (0,0), (-1,-1), 0.5, colors.black),
            ]))
            self.Story.append(table)
        self.Story.append(Spacer(1, 1 * cm))

        template = [
            ['Перечень приборов'],
            [
                '№<br/>п/п', 'Тип прибора', 'Заводской номер<br/>прибора',
                'Свидетельство о<br/>поверке', 'Дата следующей<br/>поверки' 
            ]
        ]
        for num, measurer in enumerate(self.data.get('measurers').get('selected'), start=1):
            meas = Measurer.objects.get(id=measurer)
            data = [num, *meas.details()]
            template.append(list(map(lambda x: str(x), data)))
        cols = len(template[0])
        rows = len(template)
        styles = [
            ['Regular Bold Center'] * cols,
            *[['Regular Center'] * cols] * (rows - 1),
        ]
        table_data = self.values(template, {})
        table = self.table(table_data, styles, [1, 3, 2, 2, 2], styleTable=True)
        table.setStyle(TableStyle([
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('SPAN', (0,0), (-1, 0)),
        ]))
        self.Story.append(table)

    def page5_6(self):
        self.Story.append(PageBreak())

        self.put('Нормативное и методическое обеспечение работ', 'Regular Bold Center', 0.5)
        table = Table(
            self.preetify(self.static_data_list('normatives.txt'), 'Paragraph', 'Paragraph Justified'),
            colWidths=self.columnize(1,9)
        )
        table.hAlign = 'LEFT'
        table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        self.Story.append(table)

    def page7(self):
        self.Story.append(PageBreak())
        self.formular('2 Документация, предоставленная заказчиком при выполнении работ')
        self.add_to_toc('ФОРМУЛЯР № 2', 'Документация, предоставленная заказчиком при выполнении работ')

        data = self.data.get('docs')
        table_data = list(map(lambda x: [x['name'], 'ДА' if x['value'] else 'НЕТ'], data))

        table = Table(
            self.preetify(table_data, 'Regular', 'Regular Center'),
            colWidths=self.columnize(8,2)
        )
        table.hAlign = 'LEFT'
        table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 0.5, colors.black),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 0.3*cm),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0.4*cm),
        ]))
        self.Story.append(table)
        self.Story.append(Spacer(1, 1 * cm))

    def page8(self):
        self.Story.append(PageBreak())
        self.formular('3 Паспортные данные')
        self.add_to_toc('ФОРМУЛЯР № 3', 'Паспортные данные')

        data = self.data.get('engine')
        engine = Engine.objects.get(name=data.get('type'))
        engine_data = engine.details()
        random_data = engine.random_data.get('moments')
        data.update(engine_data, connection=str(self.connection))

        template = [
            ['Тип', '{name}'],
            ['Исполнение по взрывозащите', '{ex}'],
            ['Допустимый диапазон температуры окружающей среды, °С', '{temp_low}ºС...+{temp_high}ºС'],
            ['Заводской номер', '{serial_number}'],
            ['Завод &ndash; изготовитель', '{factory}'],
            ['Год изготовления', '{manufactured_at}'],
            ['Год ввода в эксплуатацию', '{started_at}'],
            ['Соединение фаз', '{connection}'],
            ['Номинальная мощность, кВт', '{power}'],
            ['Номинальное напряжение, В', '{voltage}'],
            ['Номинальный ток статора, А', '{current}'],
            ['Номинальная частота вращения, об/мин', '{freq}'],
            ['Отношение номинального значения начального пускового момента к номинальному вращающему моменту', str(random_data.get('fraction_nominal_moment'))],
            ['Отношение начального пускового тока к номинальному току', str(random_data.get('fraction_initial_current'))],
            ['Отношение максимального вращающего момента к номинальному вращающему моменту', str(random_data.get('fraction_max_spin_moment'))],
            ['Коэффициент полезного действия, %', '{kpd}'],
            ['Коэффициент мощности, cosφ', '{coef_power}'],
            ['Класс нагревостойкости изоляции', '{warming_class}'],
            ['Масса двигателя, кг', '{weight}']
        ]
        para_style = (('Regular', 'Regular Center'), )
        table_style = (
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('TOPPADDING', (0,0), (-1,-1), 2),
        )
        self.add(template, [5, 5], self.get_style(para_style, template), table_style,
            data=data, styleTable=True
        )

    def page9(self):
        self.Story.append(PageBreak())
        self.formular('4 Данные заводских замеров и приёмо-сдаточных испытаний')
        self.add_to_toc('ФОРМУЛЯР № 4', 'Данные заводских замеров и приёмо-сдаточных испытаний')
    
        resistance_isolation = self.data['values']['factory_values']['resistance_isolation']
        resistance_phase = self.data['values']['factory_values']['resistance_phase']

        table_data = [
            ['Показатели', 'Заводские замеры', '', '',
                'Приемо-сдаточные испытания', '', '', 'Установленная норма'],
            ['',           'Фаза A', 'Фаза B', 'Фаза C', 'Фаза A', 'Фаза B', 'Фаза C', ''],
            ['Сопротивление изоляции обмотки статора относительно корпуса двигателя, МОм',
             *([resistance_isolation] * 6), 'не менее 1,0'],
            ['Сопротивление фазы обмотки статора постоянному току в холодном состоянии при 20°C, Ом',
             *([resistance_phase] * 6), 'Разница не более  2% от заводских данных'],
            ['Средняя величина воздушного зазора (односторонняя), мм', '&ndash;', '', '', '&ndash;', '', '', 
                'Разница не более  10% от среднего значения'],
            ['Эффективное значение виброскорости подшипниковых опор, мм/с', '1,2', '', '', '&ndash;',
                '', '', 'Не более 4,5 мм/с']
        ]

        rows = len(table_data)
        cols = len(table_data[0])
        table = Table(
            self.tabelize(table_data, [['Regular Center'] * cols] * rows),
            colWidths=self.columnize(2, 1, 1, 1, 1, 1, 1, 2)
        )
        table.hAlign = 'LEFT'
        table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 0.5, colors.black),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('SPAN', (1,0), (3,0)),
            ('SPAN', (4,0), (6,0)),
            ('SPAN', (0,0), (0,1)),
            ('SPAN', (7,0), (7,1)),
            ('SPAN', (1,4), (3,4)),
            ('SPAN', (4,4), (6,4)),
            ('SPAN', (1,5), (3,5)),
            ('SPAN', (4,5), (6,5)),
        ]))
        self.Story.append(table)
        text = 'Примечание: нормы согласно РД 34.45-51.300-97 «Объем и нормы испытаний электрооборудования». Издание шестое, М., «ЭНАС», 1997.'
        self.Story.append(Spacer(1, 0.5 * cm))
        self.put(text, 'Regular Justified', 1)

    def page10(self):
        self.Story.append(PageBreak())

        self.formular('5 Общий вид электродвигателя')
        self.add_to_toc('ФОРМУЛЯР № 5', 'Общий вид электродвигателя')
        self.put('Взрывозащищённый электродвигатель ' + self.data['engine']['type'], 'Regular Bold Center', .7)

        image = FileStorage.objects.get(pk=int(self.data['files']['main'][0]['id']))
        self.put_photo(image.fileupload, height=22)

    def page11(self):
        self.Story.append(PageBreak())

        self.formular('6 Конструктивная схема электродвигателя')
        self.add_to_toc('ФОРМУЛЯР № 6', 'Конструктивная схема электродвигателя. Электрическая схема подключения электродвигателя')
        engine = Engine.objects.get(name=self.data['engine']['type'])
        self.put_photo(engine.scheme, height=10)
        self.spacer(1)

        # Until paste into report only the first connection type's picture
        self.formular('6-1 Электрическая схема подключения электродвигателя')
        self.put_photo(self.connection.scheme, height=10)

    def page12(self):
        self.Story.append(PageBreak())

        self.formular('7 Тепловизионный контроль. Определение соответствия электродвигателя температурному классу')
        self.add_to_toc('ФОРМУЛЯР № 7', 'Тепловизионный контроль. Определение соответствия электродвигателя температурному классу')

        image1 = self.fetch_image(
            FileStorage.objects.get(pk=self.data['files']['therm1'][0]['id']).fileupload,
            height=10, width=9.7
        )
        image2 = self.fetch_image(
            FileStorage.objects.get(pk=self.data['files']['therm2'][0]['id']).fileupload,
            height=10, width=9.7
        )
        table_data = [[image1, image2]]
        table = Table(table_data,colWidths=self.columnize(5, 5))
        table.hAlign = 'CENTER'
        table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ]))
        self.Story.append(table)
        self.spacer(0.5)

        therm_data = self.data['therm']
        tc = ThermClass.objects.get(pk=therm_data['tclass'])
        therm_data.update(dict(tclass=tc.get_name_display(), tclass_t_max=str(tc.t_max)))

        data = [
            ['Температурный класс', '{tclass}'],
            ['Максимально допустимая температура поверхности оболочки, °C', '{tclass_t_max}'],
            ['Расстояние до объекта, м', '{distance}'],
            ['Температура окружающей среды, °С', '{temp_env}'],
            ['Максимальная температура, °С', '{temp_max}'],
            ['Минимальная температура, °С', '{temp_min}'],
            ['Средняя температура, °С', '{temp_avg}'],
            ['Соответствие норме', '{correct}'],
        ]
        rows = len(data)
        table_data = self.values(data, therm_data)
        table = self.table(table_data, [['Regular', 'Regular Center']] * rows, [8, 2], styleTable=True)
        self.Story.append(table)

    def page13(self):
        self.Story.append(PageBreak())

        self.formular('8 Вибрационный контроль электродвигателя')
        self.add_to_toc('ФОРМУЛЯР № 8', 'Вибрационный контроль электродвигателя')
        text = 'Среднеквадратичные значения виброскоростей  ротора в собственных опорах, мм/с'
        self.put(text, 'Regular Bold Center', 0.5)

        template = [
            ['Зона контроля', 'Вертикальная', 'Горизонтальная', 'Осевая'],
            ['Подшипниковый узел со стороны привода', '{vert}', '{horiz}', '{axis}'],
            ['Подшипниковый узел с противоположной приводу стороны', '{reverse_vert}', '{reverse_horiz}', '{reverse_axis}'],
            ['Норма', '{norm}', '', ''],
        ]
        para_style = [
            ['Regular Bold Center'],
            *[['Regular'] + ['Regular Center'] * 3]
        ]
        table_style = (
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('SPAN', (1,3), (3,3)),
        )
        self.add(template, [4, 2, 2, 2], self.get_style(para_style, template), table_style,
            data=self.data['vibro'], styleTable=True, spacer=.5
        )

        template = [
            ['Зона контроля', 'Соответствие норме'],
            ['Подшипники', 'соответствует'],
            ['Установка электродвигателя на раму агрегата', 'соответствует'],
            ['Дисбаланс ротора', 'соответствует'],
        ]
        para_style = [
            ['Regular Bold Center'],
            ['Regular', 'Regular Center']
        ]
        table_style = (
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        )
        self.add(template, [5, 5], self.get_style(para_style, template), table_style,
            styleTable=True, spacer=.5
        )

        self.Story.append(Spacer(1, 0.5 * cm))
        self.put('Замеры проводились на подшипниковых узлах в трёх направлениях.', 'Regular')
        text = '''
Вибродиагностический контроль электродвигателя проводился в соответствии с требованиями ГОСТ Р ИСО 10816-3-99 "Вибрация. Контроль состояния машин по результатам измерения вибрации на невращающихся частях. Часть 3. Промышленные машины номинальной мощностью более 15 кВт и номинальной скоростью от 120 до 15000 мин -1".
        '''
        self.Story.append(Spacer(1, 0.5 * cm))
        self.put(text, 'Paragraph Justified Indent')

    def page14(self):
        self.Story.append(PageBreak())
        self.formular('9-1 Визуальный и измерительный контроль электродвигателя')
        self.add_to_toc('ФОРМУЛЯР № 9-1', 'Визуальный и измерительный контроль электродвигателя')

        table_data = [[
            self.fetch_static_image('engine_details_scheme_1.jpg', 6.2),
            self.fetch_static_image('engine_details_scheme_2.jpg', 6.2),
            self.fetch_static_image('engine_details_scheme_3.jpg', 6.2),
        ]]
        table = Table(table_data) 
        table.hAlign = 'CENTER'
        self.Story.append(table)
        self.spacer(0.5)

        engine = Engine.objects.get(name=self.data['engine']['type'])
        data = engine.random_data.get('moveable_Ex_connections')
        template = [
            ['№ п/п', 'Подвижное взрывонепроницаемое соединение', 'L1, мм', 'D, мм', 'd, мм', 'W1, мм', 'S, Ra'],
            ['1', 'Узел взрывозащиты подшипникового узла со стороны привода', '{top_point[L1]}', '{top_point[D]}', '{top_point[d]}', '{top_point[W1]}', '{top_point[S]}'],
            ['2', 'Узел взрывозащиты подшипникового узла с противоположной приводу стороны', '{bottom_point[L1]}', '{bottom_point[D]}', '{bottom_point[d]}', '{bottom_point[W1]}', '{bottom_point[S]}'],
        ]
        table_style = (
            ('TOPPADDING', (0,0), (-1,-1), 0),
        )
        para_style = (
            ('Regular Bold Center', ), ('Regular Center', ),
        )
        self.add(template, [1, 4, 1, 1, 1, 1, 1], self.get_style(para_style, template), table_style,
            data=data, styleTable=True, spacer=.5
        )

        data = engine.random_data.get('unmoveable_Ex_connections')
        template = [
            ['№ п/п', 'Неподвижное взрывонепроницаемое соединение', 'L1, мм', 'L2, мм', 'W1, мм', 'b, мм', 'a, мм', 'f, мм', 'S, Ra'],
            ['1', 'Выводное устройство &ndash; крышка', '{out_krishka[L1]}', '{out_krishka[L2]}', '{out_krishka[W1]}', '{out_krishka[b]}', '{out_krishka[a]}', '{out_krishka[f]}', '{out_krishka[S]}'],
            ['2', 'Выводное устройство &ndash; станина', '{out_stanina[L1]}', '{out_stanina[L2]}', '{out_stanina[W1]}', '{out_stanina[b]}', '{out_stanina[a]}', '{out_stanina[f]}', '{out_stanina[S]}'],
            ['3', 'Крышка узла взрывозащиты &ndash; подшипниковый щит со стороны привода', '{cap_shield[L1]}', '{cap_shield[L2]}', '{cap_shield[W1]}', '{cap_shield[b]}', '{cap_shield[a]}', '{cap_shield[f]}', '{cap_shield[S]}'],
            ['4', 'Крышка узла взрывозащиты &ndash; подшипниковый щит с противоположной приводу стороны', '{cap_shield_reverse[L1]}', '{cap_shield_reverse[L2]}', '{cap_shield_reverse[W1]}', '{cap_shield_reverse[b]}', '{cap_shield_reverse[a]}', '{cap_shield_reverse[f]}', '{cap_shield_reverse[S]}'],
        ]
        self.add(template, [1, 2, 1, 1, 1, 1, 1, 1, 1], self.get_style(para_style, template), table_style,
            data=data, styleTable=True
        )

        template = [
            ['Зазор между лопастями вентилятора и защитным кожухом',
            'Не менее 1/100 максимального диаметра вентилятора согласно п.17.3 ГОСТ Р 51330.0'],
            ['Наружные и внутренние контактные зажимы заземляющих проводников',
            'Обеспечивают подсоединение проводника сечением не менее 4 мм² согласно п. 15.4 ГОСТ Р 51330.0']
        ]
        para_style = (('Regular', ), )
        self.add(template, [4, 6], self.get_style(para_style, template), table_style,
            styleTable=True, spacer=1
        )

    def page15(self):
        self.Story.append(PageBreak())

        template = [
            ['Статор', ''],
            ['Наличие истирания изоляции обмотки и токоподводов', 'нет'],
            ['Признаки перегрева изоляции обмотки и токоподводов', 'нет'],
            ['Наличие повреждений активной стали', 'нет'],
            ['Наличие пыли, масла, механических повреждений на лобовых частях обмотки статора и токоподводах', 'нет'],
        ]
        cols = len(template[0])
        rows = len(template)
        styles = [
            ['Regular Bold Center'],
            *[['Regular', 'Regular Center']] * (rows - 1)
        ]
        table_data = self.values(template, {})
        table = self.table(table_data, styles, [7, 3])
        table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 0.5, colors.black),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('SPAN', (0,0), (1,0))
        ]))
        self.Story.append(table)
        self.Story.append(Spacer(1, 0.5 * cm))

        template = [
            ['Ротор', ''],
            ['Наличие коррозии и механических повреждений на наружной поверхности вала бочки ротора и крыльчатки', 'нет'],
            ['Наличие коррозии и механических повреждений на наружных поверхностях деталей подшипников качения', 'нет'],
            ['Отсутствие свободного вращения ротора в собранном двигателе от руки', 'нет'],
        ]
        cols = len(template[0])
        rows = len(template)
        styles = [
            ['Regular Bold Center'],
            *[['Regular', 'Regular Center']] * (rows - 1)
        ]
        table_data = self.values(template, {})
        table = self.table(table_data, styles, [7, 3])
        table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 0.5, colors.black),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('SPAN', (0,0), (1,0))
        ]))
        self.Story.append(table)

    def page16(self):
        self.Story.append(PageBreak())
        self.formular('9-2 Контроль параметров взрывозащиты')
        self.add_to_toc('ФОРМУЛЯР № 9-2', 'Контроль параметров взрывозащиты')

        self.put('Взрывонепроницаемая оболочка', 'Regular Bold Center', 0.4)
        template = [
            ['Отсутствие маркировки и предупреждающих знаков', 'нет'],
            ['Наличие коррозии и механических повреждений на взрывонепроницаемых поверхностях взрывонепроницаемой оболочки', 'нет'],
            ['Наличие механических повреждений (сколы, трещины, вмятины) на деталях взрывонепроницаемой оболочки', 'нет'],
            ['Отсутствие крепёжных элементов', 'нет'],
            ['Среднее число полных неповрежденных непрерывных ниток резьбы', '8'],
            ['Качество резьбы', 'хорошее'],
            ['Затяжка крепёжных болтов', 'хорошее'],
            ['Наличие следов эрозии и коррозии на резьбовых соединениях', 'нет'],
            ['Наличие коррозии и механических повреждений на крышке и корпусе выводного устройства', 'нет'],
            ['Наличие повреждений прокладок', 'нет'],
            ['Отсутствие антикоррозионной смазки  на взрывонепроницаемых поверхностях', 'нет'],
            ['Наличие повреждений уплотнительного кольца кабельного ввода', 'нет']
        ]
        cols = len(template[0])
        rows = len(template)
        styles = [
            *[['Regular', 'Regular Center']] * rows
        ]
        table_data = self.values(template, {})
        table = self.table(table_data, styles, [8, 2], styleTable=True)
        table.setStyle(TableStyle([
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ('TOPPADDING', (0,0), (-1,-1), 5),
        ]))
        self.Story.append(table)


    def page17(self):
        self.Story.append(PageBreak())
        self.formular('10 Ультразвуковая дефектоскопия и толщинометрия взрывозащищённой оболочки электродвигателя')
        self.add_to_toc('ФОРМУЛЯР № 10', 'Ультразвуковая дефектоскопия и толщинометрия взрывозащищённой оболочки электродвигателя')

        engine = Engine.objects.get(name=self.data['engine']['type'])
        self.put_photo(engine.meters, height=11)
        #self.Story.append(Spacer(1, 1 * cm))

        zones_data = engine.control_zones()
        template = [
            ['1 &ndash; {control_zone_1}'],
            ['2 &ndash; {control_zone_2}'],
            ['3 &ndash; {control_zone_3}'],
            ['4 &ndash; {control_zone_4}'],
        ]
        rows = len(template)
        styles = [
            *[['Regular']] * rows
        ]
        table_data = self.values(template, zones_data)
        table = self.table(table_data, styles, [8, 2])
        table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 0)
        ]))
        table.hAlign = 'RIGHT'
        self.Story.append(table)
        self.Story.append(Spacer(1, 0.5 * cm))

        self.put('Техническое состояние элементов', 'Regular Bold Center', 0.4)
        template = [
            ['Зона контроля', 'Толщина основного металла, мм', '', '', 'Дефекты', ''],
            ['', 'фактическая', 'норма (не менее)', 'соотв. норме', 'основного металла', 'сварных соединений'],
            ['{control_zone_1_cap}', '{control_zone_1_real}', '{control_zone_1_norm}'] + ['соответствует'] * 3,
            ['{control_zone_2_cap}', '{control_zone_2_real}', '{control_zone_2_norm}'] + ['соответствует'] * 3,
            ['{control_zone_3_cap}', '{control_zone_3_real}', '{control_zone_3_norm}'] + ['соответствует'] * 3,
            ['{control_zone_4_cap}', '{control_zone_4_real}', '{control_zone_4_norm}'] + ['соответствует'] * 3,
        ]
        para_style = (
            ('Regular Bold Center',),
            ('Regular Bold Center',),
            ['Regular', *['Regular Center'] * 5],
        )
        engine = Engine.objects.get(name=self.data['engine']['type'])
        zones_data = engine.control_zones()
        table_style = (
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('SPAN', (0,0), (0, 1)),
            ('SPAN', (1,0), (3, 0)),
            ('SPAN', (4,0), (5, 0)),
        )
        self.add(template, [3, 1, 1, 1, 2, 2], self.get_style(para_style, template), table_style,
            data=zones_data, styleTable=True, spacer=.5
        )

    def page18(self):
        self.Story.append(PageBreak())
        self.formular('11 Измерение сопротивления обмотки статора постоянному току')
        self.add_to_toc('ФОРМУЛЯР № 11', 'Измерение сопротивления обмотки статора постоянному току')
        self.put('Схема подключения прибора', 'Regular Center', 0.2)
        img = self.fetch_static_image('meter_scheme.gif', height=5)
        img.hAlign = 'CENTER'
        self.Story.append(img)
        self.Story.append(Spacer(1, 0.5 * cm))
        template = [
            ['Фаза', 'А-В', 'B-C', 'C-A'],
            ['Сопротивление обмотки, Ом', '{wireAB}', '{wireBC}', '{wireCA}'],
            ['Соответствие норме', 'соответствует', '', ''],
        ]
        cols = len(template[0])
        rows = len(template)
        styles = [
            ['Regular Bold Center'] * cols,
            *[['Regular'] + ['Regular Center'] * (cols - 1)] * (rows - 1),
        ]
        table_data = self.values(template, self.data['resistance'])
        table = self.table(table_data, styles, [4, 2, 2, 2], styleTable=True)
        table.setStyle(TableStyle([
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('SPAN', (1,2), (3, 2)),
        ]))
        self.Story.append(table)
        self.Story.append(Spacer(1, 0.5 * cm))

        self.put('Измерение проведено в соответствии с требованиями п. 1.8.15. «Правила устройства электроустановок» 7-е издание.', 'Paragraph Justified', 0.2)
        self.Story.append(Spacer(1, 1 * cm))

        self.formular('12 Измерение сопротивления изоляции обмотки статора')
        self.add_to_toc('ФОРМУЛЯР № 12', 'Измерение сопротивления изоляции обмотки статора')
        self.put('Упрощенная схема подключения мегаомметра', 'Regular Center', 0.2)
        img = self.fetch_static_image('megaommetr_scheme.jpg', height=3.5)
        img.hAlign = 'CENTER'
        self.Story.append(img)
        self.Story.append(Spacer(1, 0.5 * cm))
        template = [
            ['Фаза', 'А-0', 'B-0', 'C-0', 'А-В', 'B-C', 'C-A'],
            ['Сопротивление изоляции, Мом', '{isolation}', '{isolation}', '{isolation}', '&ndash;', '&ndash;', '&ndash;'],
            ['Соответствие норме', 'соответствует', '', '', '', '', ''],
        ]
        cols = len(template[0])
        rows = len(template)
        styles = [
            ['Regular Bold Center'] * cols,
            *[['Regular'] + ['Regular Center'] * (cols - 1)] * (rows - 1),
        ]
        table_data = self.values(template, self.data['resistance'])
        table = self.table(table_data, styles, [4, 1, 1, 1, 1, 1, 1], styleTable=True)
        table.setStyle(TableStyle([
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('SPAN', (1,2), (6, 2)),
        ]))
        self.Story.append(table)
        self.Story.append(Spacer(1, 0.5 * cm))

        self.put('Измерение проведено согласно табл. 5.1-5.3 РД 34.45-51.300-97 «Объем и нормы испытаний электрооборудования».', 'Paragraph Justified')

    def page19(self):
        self.Story.append(PageBreak())
        self.formular('13 Рекомендации по ремонту и эксплуатации')
        self.add_to_toc('ФОРМУЛЯР № 13', 'Рекомендации по ремонту и эксплуатации')

        self.put('В соответствии с требованиями нормативной документации и с результатами диагностики и исследований необходимо:', 'Paragraph Justified', 0.2)

        text = self.static_data_list('recommendations.txt')
        data = self.values(text, self.data['engine'])
        table = Table(
            self.preetify(data, 'Paragraph', 'Paragraph Justified'),
            colWidths=self.columnize(1,9)
        )
        table.hAlign = 'LEFT'
        table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        self.Story.append(table)

    def page20(self):
        self.Story.append(PageBreak())
        self.formular('14 Заключение')
        self.add_to_toc('ФОРМУЛЯР № 14', 'Заключение')

        template = self.static_data_plain('decision.txt')
        cols = len(template[0])
        rows = len(template)
        styles = [
            *[['Paragraph Justified Indent'] * cols] * rows
        ]
        table_data = self.values(template, self.data['engine'])
        table = self.table(table_data, styles, [10])
        table.setStyle(TableStyle([
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ]))
        self.Story.append(table)

    def page21(self):
        self.Story.append(PageBreak())
        self.formular('15 Выполненные мероприятия в процессе проведения работ')
        self.add_to_toc('ФОРМУЛЯР № 15', 'Выполненные мероприятия в процессе проведения работ')

        self.put('В процессе технического диагностирования были проведены следующие мероприятия:', 'Paragraph', 0.2)
        text = self.static_data_list('completed_tasks.txt')
        data = self.values(text, self.data['engine'])
        table = Table(
            self.preetify(data, 'Paragraph', 'Paragraph Justified'),
            colWidths=self.columnize(1,9)
        )
        table.hAlign = 'LEFT'
        table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
        ]))
        self.Story.append(table)

    def appendix(self, title, columns, widths):
        self.Story.append(PageBreak())
        self.formular(title, header='Приложение')
        num, *tail = title.split()
        self.add_to_toc('ПРИЛОЖЕНИЕ ' + num, ' '.join(tail))
        template = [
            columns,
            *[['&nbsp;'] * len(columns)] * 36
        ]
        rows = len(template)
        cols = len(template[0])
        styles = [
            *[['Regular Bold Center'] * cols] * rows
        ]
        table_data = self.values(template, {})
        table = self.table(table_data, styles, widths)
        table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 0.5, colors.black),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 0),
        ]))
        self.Story.append(table)

    def setup_page_templates(self, doc):
        frame_full = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='no_header')
        template_title = PageTemplate(id='Title', frames=frame_full)

        print('obj_data', self.data['obj_data'])
        frame_with_header = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height-2*cm,
                bottomPadding=0, leftPadding=0, rightPadding=0, topPadding=0,
                id='with_header')
        header_content = Paragraph('''{org[name]} {lpu[name]} {ks} {location} {plant}
            станционный №{station_number} зав.№{serial_number}'''.format(
                **self.data['obj_data'], **self.data['engine']
            ), self.styles["Page Header"]
        )
        template_content = PageTemplate(id='Content', frames=frame_with_header, onPage=partial(self.header, content=header_content))

        doc.addPageTemplates([template_title, template_content])

    @staticmethod
    def header(canvas, doc, content):
        canvas.saveState()

        style = PS(
            'Page Number',
            fontName='Times',
            fontSize=13)
        pageNumber = Paragraph(str(canvas.getPageNumber()), style=style)
        w, h = pageNumber.wrap(doc.width, doc.topMargin)
        pageNumber.drawOn(canvas, doc.width + doc.leftMargin - 10, h + 10)

        w, h = content.wrap(doc.width, doc.topMargin)
        content.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)

        canvas.restoreState()

