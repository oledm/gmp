from datetime import datetime

from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, XPreformatted
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase import ttfonts

from gmp.authentication.models import Employee
from gmp.certificate.models import Certificate
from gmp.inspections.models import Organization, LPU
from gmp.departments.models import Measurer
from gmp.engines.models import Engine

class Report():
    def __init__(self, data):
        self.full_width = 18.7
        self.data = data
        self.investigation_date = self.data.get('investigationDate').split(',')[0]
        self.date_begin = self.data.get('workBegin').split(',')[0]
        self.date_end = self.data.get('workEnd').split(',')[0]
        self.Story = []

        #lpu = LPU.objects.get(name=self.data.get('lpu'))
        self.obj_data = self.data['obj_data']
        self.styles = getSampleStyleSheet()

    def make_report(self, report):
        doc = SimpleDocTemplate(report, pagesize=A4,
                                rightMargin=12,leftMargin=12,
                                topMargin=12,bottomMargin=12,
                                title='Паспорт двигателя ' + self.data['engine']['type'],
                                #showBoundary=1,
        )
         
        self.setup_fonts()
        self.setup_styles()


        self.page1()
        self.page3()
        self.page2()
        self.page7()
        self.page8()
            
        doc.build(self.Story)

    def page1(self):
        ptext = 'ПАО "ГАЗПРОМ"<br/>РОССИЙСКАЯ ФЕДЕРАЦИЯ<br/>ООО «ГАЗМАШПРОЕКТ»'
            
        doc.build(self.Story)

    def page1(self):
        ptext = 'ПАО "ГАЗПРОМ"<br/>РОССИЙСКАЯ ФЕДЕРАЦИЯ<br/>ООО «ГАЗМАШПРОЕКТ»'
        self.Story.append(Paragraph(ptext, self.styles["Heading 1 Bold"]))
        self.Story.append(Spacer(1, 0.5 * cm))

        ptext = '''<b>"Согласовано"</b><br/><br/>
        Заместитель генерального директора по производству - Главный инженер 
        Шеморданского ЛПУ МГ<br/>
        ООО"Газпром трансгаз Ставрополь"
        '''
        left_column = Paragraph(ptext, self.styles["Heading 1"]) 
        ptext = '''<b>"Утверждаю"</b><br/><br/>
        Директор филиала<br/>
        ООО «ГАЗМАШПРОЕКТ»<br/>
        «НАГАТИНСКИЙ»
        '''
        right_column = Paragraph(ptext, self.styles["Heading 1"]) 
        table_data = [[left_column, right_column]]
        
        ptext = '''___________________Ю.В. Иванов
"____"_________________201     г.
        '''
        left_column = XPreformatted(ptext, self.styles["Signature Handwrite"]) 
        ptext = '''_______________А.Н. Бондаренко
"____"_________________201     г.
        '''
        right_column = XPreformatted(ptext, self.styles["Signature Handwrite"]) 
        table_data.extend([[left_column, right_column]])
        table = Table(table_data)
        table.setStyle(TableStyle([
            #('INNERGRID', (0,0), (-1,-1), 0.1, colors.black),
            #('BOX', (0,0), (-1,-1), 1.0, colors.black),

            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('RIGHTPADDING', (0,0), (0,-1), 1.5*cm),
            ('LEFTPADDING', (-1,0), (-1,-1), 1.5*cm),
        ]))
        self.Story.append(table)
        self.Story.append(Spacer(1, 1.3 * cm))

        self.mput([
            'ПАСПОРТ 1-2/1715-10-14',
            'ТЕХНИЧЕСКОГО СОСТОЯНИЯ',
            'ВЗРЫВОЗАЩИЩЁННОГО ЭЛЕКТРОДВИГАТЕЛЯ',
        ], 'MainTitle', 1)

        text = '''ОБЪЕКТ: {org}<br/>{lpu}<br/>{ks}<br/>{plant}<br/>
            станционный № {station_number}<br/>
            ТИП: {type} зав.№ {serial_number}'''.format(
                **self.obj_data, **self.data.get('engine')
        )
        self.put(text, 'MainTitle', 1)

        self.put('Дата обследования: ' + self.investigation_date, 'Heading 1', 1)
        self.Story.append(Spacer(1, 1 * cm))

        ptext = '''Заместитель начальника отдела ДОЭ<br/>
        Шеморданского ЛПУ МГ<br/>
        ООО"Газпром трансгаз Ставрополь"
        '''
        left_column = Paragraph(ptext, self.styles["Heading 1"]) 
        ptext = '''Начальник проектно-<br/>
        диагностического отдела<br/>
        ООО «ГАЗМАШПРОЕКТ»<br/>
        «НАГАТИНСКИЙ»
        '''
        right_column = Paragraph(ptext, self.styles["Heading 1"]) 
        table_data = [[left_column, right_column]]
        
        ptext = '''___________________П.Д. Петров
"____"_________________201     г.
        '''
        left_column = XPreformatted(ptext, self.styles["Signature Handwrite"]) 
        ptext = '''________________И.Ю. Медведев
"____"_________________201     г.
        '''
        right_column = XPreformatted(ptext, self.styles["Signature Handwrite"]) 
        table_data.extend([[left_column, right_column]])
        table = Table(table_data)
        table.setStyle(TableStyle([
            #('INNERGRID', (0,0), (-1,-1), 0.1, colors.black),
            #('BOX', (0,0), (-1,-1), 1.0, colors.black),

            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('RIGHTPADDING', (0,0), (0,-1), 1.5*cm),
            ('LEFTPADDING', (-1,0), (-1,-1), 1.5*cm),
        ]))
        self.Story.append(table)

    def page2(self):
        self.Story.append(PageBreak())
        self.page_header()

        table_data = [
            ['Список сертифицированных членов бригады'],
            [
                '№\nп/п', 'Фамилия И.О.', '№ квалифика-\nционного\nудостоверения',
                'Дата\nвыдачи', 'Срок\nдейст-\nвия', 'Виды\nконтроля', 'Уровень', 'Группа\nЭБ'
            ]
        ]

        for num, person in enumerate(self.data.get('team'), start=1):
            emp = Employee.objects.get_by_full_name(person['name'])
            cert = Certificate.objects.get(employee=emp)
            row_data = [num, emp.fio()]
            row_data.extend(cert.details())
            table_data.append(row_data)

        table = Table(table_data, colWidths=[1.7 * cm, 3.8 * cm, 3.8 * cm,
            1.85 * cm, 1.85 * cm, 1.85 * cm, 1.85 * cm, 1.85 * cm])
        table.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), 'Times'),
            ('FONTSIZE', (0,0), (-1,-1), 12),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEADING', (0,0), (-1,-1), 16),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
            ('BOX', (0,0), (-1,-1), 0.5, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),

            ('SPAN', (0,0), (-1,0)),
            ('FONTNAME', (0,0), (-1,0), 'Times Bold'),
            ('TOPPADDING', (0,0), (-1,0), 8),
            ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ]))
        self.Story.append(table)
        self.Story.append(Spacer(1, 0.5 * cm))

        table_data = [
            ['Перечень приборов'],
            [
                '№\nп/п', 'Тип прибора', 'Заводской номер\nприбора',
                'Свидетельство о\nповерке', 'Дата следующей\nповерки' 
            ]
        ]

        for num, measurer in enumerate(self.data.get('measurers'), start=1):
            meas = Measurer.objects.get(id=measurer['id'])
            row_data = [num, *map(lambda p: Paragraph(p, self.styles['Normal Center']), meas.details())]
            table_data.append(row_data)

        table = Table(table_data, colWidths=[1.7 * cm, 5.7 * cm, 3.75 * cm, 3.85 * cm, 3.65 * cm])
        table.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), 'Times'),
            ('FONTSIZE', (0,0), (-1,-1), 12),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEADING', (0,0), (-1,-1), 16),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
            ('BOX', (0,0), (-1,-1), 0.5, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),

            ('SPAN', (0,0), (-1,0)),
            ('FONTNAME', (0,0), (-1,0), 'Times Bold'),
            ('TOPPADDING', (0,0), (-1,0), 8),
            ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ]))
        self.Story.append(table)

    def page3(self):
        self.Story.append(PageBreak())
        self.page_header()
        self.formular('1 Регистрация работ')

        ptext = '<b>Фамилия И.О.</b><br/>' + '<br/>'.join(
                [x.get('name') for x in self.data.get('team')]
        )
        left = Paragraph(ptext, self.styles['Table Content']) 
        ptext = '<b>Должность</b><br/>' + '<br/>'.join(
                [x.get('rank') for x in self.data.get('team')]
        )
        right = Paragraph(ptext, self.styles['Table Content']) 
        team_table = Table([[left, right]])
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

        text = '\n'.join(['____________________' + x.get('name') for x in self.data.get('team')])
        table2 = Table([[Paragraph(text, self.styles['Signature Left'])]])
        table2.setStyle(style)

        table_data = [
            ['ВИД РАБОТ', 'Техническое диагностирование'],
            ['ДАТА НАЧАЛА', self.date_begin],
            ['ДАТА ОКОНЧАНИЯ', self.date_end],
            [Paragraph('СОСТАВ БРИГАДЫ СПЕЦИАЛИСТОВ', self.styles['Regular Bold Center']), team_table],
            ['ОРГАНИЗАЦИЯ', 'ООО "ГАЗМАШПРОЕКТ"'],
            ['РАЗРЕШЕНИЕ', '''Свидетельство об аккредитации 766-Э/ТД выдано Управлением\nэнергетики ОАО "Газпром" 11 февраля 2015 г.\nСрок действия до 11 февраля 2018 г.'''],
            ['СУБПОДРЯДНАЯ\nОРГАНИЗАЦИЯ', ''],
            ['РАЗРЕШЕНИЕ\nСУБПОДРЯДНОЙ\nОРГАНИЗАЦИИ', ''],
            ['ПОДПИСИ\nЧЛЕНОВ\nБРИГАДЫ', table2],
        ]

        table = Table(table_data, colWidths=self.columnize(3,7))
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
        self.Story.append(Spacer(1, 1 * cm))

    def page8(self):
        self.Story.append(PageBreak())
        self.page_header()
        self.formular('3 Паспортные данные')

        data = self.data.get('engine')
        serial = data.get('serial_number')
        manufactured = data.get('manufactured_at')
        started = data.get('started_at')
        engine = Engine.objects.get(name=data.get('type'))
        moments = engine.random_data.get('moments')

        table_data = [
            ['Тип', engine.name],
            ['Исполнение по взрывозащите', str(engine.ex)],
            ['Допустимый диапазон температуры окружающей среды, °С', '{}ºС...+{}ºС'.format(engine.temp_low, engine.temp_high)],
            ['Заводской номер', serial],
            ['Завод – изготовитель', str(engine.factory)],
            ['Год изготовления', manufactured],
            ['Год ввода в эксплуатацию', started],
            ['Соединение фаз', str(engine.connection.get())],
            ['Номинальная мощность, кВт', '{0:g}'.format(engine.power)],
            ['Номинальное напряжение, В', str(engine.voltage)],
            ['Номинальный ток статора, А', '{0:g}'.format(engine.current)],
            ['Номинальная частота вращения, об/мин', str(engine.freq)],
            ['Отношение номинального значения начального пускового момента к номинальному вращающему моменту', str(engine.freq)],
            ['Отношение начального пускового тока к номинальному току', str(moments.get('fraction_initial_current'))],
            ['Отношение максимального вращающего момента к номинальному вращающему моменту', str(moments.get('fraction_max_spin_moment'))],
            ['Коэффициент полезного действия, %', '{0:g}'.format(engine.kpd)],
            ['Коэффициент мощности, cosφ', '{0:g}'.format(engine.coef_power)],
            ['Класс нагревостойкости изоляции', str(engine.warming_class)],
            ['Масса двигателя, кг', str(engine.weight)],
        ]

        table = Table(
            self.preetify(table_data, 'Regular', 'Regular Center'),
            colWidths=self.columnize(5,5)
        )
        table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 0.5, colors.black),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        self.Story.append(table)
        self.Story.append(Spacer(1, 1 * cm))

    def page7(self):
        self.Story.append(PageBreak())
        self.page_header()
        self.formular('2 Документация, предоставленная заказчиком при выполнении работ')

        data = self.data.get('docs')
        table_data = list(map(lambda x: [x['name'], 'ДА' if x['value'] else 'НЕТ'], data))

        table = Table(
            self.preetify(table_data, 'Regular', 'Regular Center'),
            colWidths=self.columnize(8,2)
        )
        table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 0.5, colors.black),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 0.3*cm),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0.4*cm),
        ]))
        self.Story.append(table)
        self.Story.append(Spacer(1, 1 * cm))
    '''
        Helper functions
    '''

    def preetify(self, lst, *style):
        return list(map(
            lambda a, b: [
                Paragraph(a, self.styles[style[0]]),
                Paragraph(b, self.styles[style[1]])
            ], *zip(*lst)
            )
        )
    def page_header(self):
        self.put('{org} {lpu}'.format(**self.obj_data), 'Page Header', 0.5)

    def formular(self, text):
        table = Table([['Формуляр № ' + text]], colWidths=[self.full_width * cm])
        table.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), 'Times Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 12),
            ('LEADING', (0,0), (-1,-1), 16),
            ('INNERGRID', (0,0), (-1,-1), 2, colors.black),
            ('BOX', (0,0), (-1,-1), 2, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ]))
        self.Story.append(table)
        self.Story.append(Spacer(1, 0.5 * cm))

    def columnize(self, *widths):
        return [self.full_width * width * 0.1 * cm for width in widths]

    def mput(self, content_list, style_name, spacer=None):
        list(map(lambda x: self.put(x, style_name), content_list))

        if spacer:
            self.Story.append(Spacer(1, spacer * cm))

    def put(self, content, style_name, spacer=None):
        self.Story.append(Paragraph(content, self.styles[style_name]))

        if spacer:
            self.Story.append(Spacer(1, spacer * cm))

    def setup_fonts(self):
        fonts = (
            ('Times', 'times.ttf'), 
            ('Times Bold', 'timesbd.ttf'),
            ('Times Italic', 'timesi.ttf'),
            ('Times Bold Italic', 'timesbi.ttf'),
        )
        list(map(self.register_font, *zip(*fonts)))
        pdfmetrics.registerFontFamily(
            'Times', normal='Times', bold='Times Bold',
            italic='Times Bold Italic', boldItalic='Times Bold Italic')

    def register_font(self, font_name, font_file):
        MyFontObject = ttfonts.TTFont(font_name, font_file)
        pdfmetrics.registerFont(MyFontObject)
     
    def setup_styles(self):
        self.styles.add(ParagraphStyle(name='Justify', alignment=TA_CENTER))
        self.styles.add(ParagraphStyle(
            name='Heading 1 Bold',
            fontName='Times Bold',
            fontSize=14,
            leading=20,
            alignment=TA_CENTER))
        self.styles.add(ParagraphStyle(
            name='Heading 1',
            fontName='Times',
            #borderWidth=0.3,
            #borderColor=colors.black,
            fontSize=13,
            leading=18,
            leftIndent=1*cm,
            alignment=TA_CENTER))
        self.styles.add(ParagraphStyle(
            name='Signature',
            fontName='Times',
            #borderWidth=0.3,
            #borderColor=colors.black,
            fontSize=13,
            leading=30,
            alignment=TA_CENTER))
        self.styles.add(ParagraphStyle(
            name='Signature Handwrite',
            fontName='Times',
            #borderWidth=0.3,
            #borderColor=colors.black,
            fontSize=13,
            leftIndent=1*cm,
            leading=30,
            alignment=TA_CENTER))
        self.styles.add(ParagraphStyle(
            name='MainTitle',
            fontName='Times Bold',
            #borderWidth=0.3,
            #borderColor=colors.black,
            fontSize=16,
            leading=20,
            alignment=TA_CENTER))
        self.styles.add(ParagraphStyle(
            name='Page Header',
            fontName='Times Bold',
            #borderWidth=0.3,
            #borderColor=colors.black,
            fontSize=13,
            alignment=TA_LEFT))
        self.styles.add(ParagraphStyle(
            name='Normal Center',
            fontName='Times',
            fontSize=13,
            alignment=TA_CENTER))
        self.styles.add(ParagraphStyle(
            name='Regular',
            fontName='Times',
            fontSize=13,
            alignment=TA_LEFT))
        self.styles.add(ParagraphStyle(
            name='Regular Bold Center',
            fontName='Times Bold',
            fontSize=13,
            alignment=TA_CENTER))
        self.styles.add(ParagraphStyle(
            name='Regular Center',
            fontName='Times',
            fontSize=13,
            alignment=TA_CENTER))
        self.styles.add(ParagraphStyle(
            name='Signature Left',
            fontName='Times',
            leading=30,
            fontSize=13,
            alignment=TA_LEFT))
        self.styles.add(ParagraphStyle(
            name='Table Content',
            fontName='Times',
            leading=16,
            fontSize=13,
            alignment=TA_LEFT))
