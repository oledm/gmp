from functools import partial
import locale
from datetime import datetime

from django.conf import settings

from PIL import Image as PILImage
import environ

from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, XPreformatted, NextPageTemplate
from reportlab.platypus.doctemplate import BaseDocTemplate, PageTemplate
from reportlab.platypus.frames import Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase import ttfonts

from gmp.authentication.models import Employee
from gmp.certificate.models import Certificate
from gmp.inspections.models import Organization, LPU
from gmp.departments.models import Measurer
from gmp.engines.models import Engine, ThermClass
from gmp.filestorage.models import UploadedFile

locale.setlocale(locale.LC_ALL, "")
loc = partial(locale.format, "%.2f")








from reportlab.platypus.flowables import Flowable
from reportlab.lib.colors import tan, green
class HandAnnotation(Flowable):
    '''A hand flowable.'''
    def __init__(self, xoffset=0, size=None, fillcolor=tan, strokecolor=green):
        from reportlab.lib.units import inch
        if size is None: size=4*inch
        self.fillcolor, self.strokecolor = fillcolor, strokecolor
        self.xoffset = xoffset
        self.size = size
        # normal size is 4 inches
        self.scale = size/(4.0*inch)

    def wrap(self, *args):
        return (self.xoffset, self.size)

    def draw(self):
        canvas = self.canv
        canvas.setLineWidth(6)
        canvas.setFillColor(self.fillcolor)
        canvas.setStrokeColor(self.strokecolor)
        canvas.translate(self.xoffset+self.size,0)
        canvas.rotate(90)
        canvas.scale(self.scale, self.scale)
        hand(canvas, debug=0, fill=1)


class DoubledLine(Flowable):
    def __init__(self, width, height=0):
        Flowable.__init__(self)
        self.width = width
        self.height = height
 
    def __repr__(self):
        return "Line(w=%s)" % self.width
 
    def draw(self):
        self.canv.line(0, self.height, self.width, self.height)
        self.canv.line(0, self.height + 2, self.width, self.height + 2)


class StaticText():
    @staticmethod
    def get_list(fname):
        file_ = str(settings.APPS_DIR.path('static', 'src', 'assets', fname))
        res = []
        with open(file_) as f:
            for n, line in enumerate(f, start=1):
                res.append([str(n), line])
        return res

    @staticmethod
    def plain(fname):
        file_ = str(settings.APPS_DIR.path('static', 'src', 'assets', fname))
        res = []
        with open(file_) as f:
            for line in f:
                res.append([line])
        return res

#class MyDocTemplate(BaseDocTemplate):
#    def __init__(self, filename, **kw):
#        BaseDocTemplate.__init__(self, filename, **kw)
#        template = PageTemplate('normal', [Frame(0, 0, 15*cm, 25*cm, id='F1')])
#        self.addPageTemplates(template)

def values(template, data):
    return list(map(lambda row: list(map(lambda cell: cell.format(**data), row)), template))

def fetch_static_image(img, size):
    file_ = str(settings.APPS_DIR.path('static', 'src', 'assets', 'images', img))
    image = PILImage.open(file_)
    ratio = float(image.width/image.height)
    return Image(file_, width=size * cm * ratio, height=size * cm)

def header(canvas, doc, content):
    canvas.saveState()
    w, h = content.wrap(doc.width, doc.topMargin)
    content.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)
    canvas.restoreState()


class Report():
    def __init__(self, data):
        self.data = data
        self.format_JS_dates(self.data, ('workBegin', 'workEnd', 'investigationDate'))
        self.format_JS_dates(self.data['engine'], ('manufactured_at', 'started_at'), '%Y')
        self.format_JS_dates(self.data['engine'], ('new_date',))

        self.date_begin = self.data.get('workBegin')
        self.date_end = self.data.get('workEnd')
        self.investigation_date = self.data.get('investigationDate')
        # Filter empty team members appeared after accident click on 'Add'
        # team's member button
        self.data['team'] = list(filter(lambda x: x['name'], self.data.get('team')))
        self.Story = []

        self.obj_data = self.data['obj_data']
        self.styles = getSampleStyleSheet()

    def format_JS_dates(self, d, keys, format_='%d.%m.%Y'):
        for key in keys:
            dt = datetime.strptime(d[key].split('T')[0], '%Y-%m-%d')
            d[key] = dt.strftime(format_)

    def make_report(self, report):
        doc = BaseDocTemplate(report, pagesize=A4,
                                rightMargin=12,leftMargin=12,
                                topMargin=12,bottomMargin=12,
                                title='Паспорт двигателя ' + self.data['engine']['type'],
                                #showBoundary=1,
        )

        self.setup_fonts()
        self.setup_styles()
        self.setup_page_templates(doc)
        self.full_width = doc.width

        self.Story.append(NextPageTemplate('Title'))
        self.page1()
        self.Story.append(NextPageTemplate('Content'))
        self.page2()
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
            
        doc.build(self.Story)

    def page1(self):
        #ptext = 'ПАО "ГАЗПРОМ"<br/>РОССИЙСКАЯ ФЕДЕРАЦИЯ<br/>ООО «ГАЗМАШПРОЕКТ»'
        #self.Story.append(Paragraph(ptext, self.styles["Heading 1 Bold"]))
        self.put('ПАО "ГАЗПРОМ"', 'Heading 1 Bold')
        self.Story.append(DoubledLine(self.full_width))
        self.put('РОССИЙСКАЯ ФЕДЕРАЦИЯ<br/>ООО «ГАЗМАШПРОЕКТ»', 'Heading 1 Bold')

        self.Story.append(Spacer(1, 0.5 * cm))

        signers = self.data['signers']['approve']
        date_string = '"____"{:_>21}'.format('_') + '201&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;г'
        fio_string = '{fio:_>32}'
        first_col = ['"Согласовано"', '{rank}', fio_string,
             date_string    
        ]
        second_col = [
            '"Утверждаю"',
            'Директор филиала<br/>ООО «ГАЗМАШПРОЕКТ» «НАГАТИНСКИЙ»',
            fio_string.format(fio='А.Н. Бондаренко'),
            date_string    
        ]
        template = list(zip(first_col, ['&nbsp;'] * len(first_col), second_col))
        cols = len(template[0])
        styles = [
            ['Heading 1 Bold'] * cols,
            ['Heading 1'] * cols,
            *[['Regular'] * cols] * 2,
        ]
        table_data = values(template, signers)
        table = self.table(table_data, styles, [4, 2, 4], styleTable=False)
        table.hAlign = 'LEFT'
        table.setStyle(TableStyle([
            ('BOTTOMPADDING', (0,0), (-1,-1), 15),
            ('BOTTOMPADDING', (0,0), (-1,0), 20),
            ('BOTTOMPADDING', (0,1), (-1,1), 20),
            #('TOPPADDING', (0,0), (-1,-1), 5),
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

        text = '''ОБЪЕКТ: {org}<br/>{lpu}<br/>{ks}<br/>{plant}<br/>{location}<br/>
            станционный № {station_number}<br/>
            ТИП: {type} зав.№ {serial_number}'''.format(
                **self.obj_data, **self.data.get('engine')
        )
        self.put(text, 'MainTitle', 1)
        self.put('Дата обследования: ' + self.investigation_date, 'Heading 1', 2)

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
        table_data = values(template, signers)
        table = self.table(table_data, styles, [4, 2, 4], styleTable=False)
        table.hAlign = 'LEFT'
        table.setStyle(TableStyle([
            ('BOTTOMPADDING', (0,0), (-1,-1), 15),
            ('BOTTOMPADDING', (0,1), (-1,1), 20),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ]))
        self.Story.append(table)

    def page2(self):
        self.Story.append(PageBreak())
        self.put('Содержание', 'Regular Bold Center', 0.5)

        data = (
            ('ФОРМУЛЯР № 1', 'Регистрация работ', '3'),
            ('ФОРМУЛЯР № 2', 'Документация, предоставленная заказчиком при выполнении работ', '7'),
            ('ФОРМУЛЯР № 3', 'Паспортные данные', '8'),
            ('ФОРМУЛЯР № 4', 'Данные заводских замеров и приёмо-сдаточных испытаний', '9'),
            ('ФОРМУЛЯР № 5', 'Общий вид электродвигателя', '10'),
            ('ФОРМУЛЯР № 6', 'Конструктивная схема электродвигателя. Электрическая схема подключения электродвигателя', '11'),
            ('ФОРМУЛЯР № 7', 'Тепловизионный контроль. Определение соответствия электродвигателя температурному классу', '12'),
            ('ФОРМУЛЯР № 8', 'Вибрационный контроль электродвигателя', '13'),
            ('ФОРМУЛЯР № 9-1', 'Визуальный и измерительный контроль электродвигателя', '14'),
            ('ФОРМУЛЯР № 9-2', 'Контроль параметров взрывозащиты', '16'),
            ('ФОРМУЛЯР № 10', 'Ультразвуковая дефектоскопия и толщинометрия взрывозащищённой оболочки электродвигателя', '17'),
            ('ФОРМУЛЯР № 11', 'Измерение сопротивления обмотки статора постоянному току', '18'),
            ('ФОРМУЛЯР № 12', 'Измерение сопротивления изоляции обмотки статора', '18'),
            ('ФОРМУЛЯР № 13', 'Рекомендации по ремонту и эксплуатации', '19'),
            ('ФОРМУЛЯР № 14', 'Заключение', '20'),
            ('ФОРМУЛЯР № 14', 'Заключение', '20'),
            ('ФОРМУЛЯР № 15', 'Выполненные мероприятия в процессе проведения работ', '21'),
            ('ПРИЛОЖЕНИЕ 1', 'Сведения об эксплуатации электродвигателя', '22'),
            ('ПРИЛОЖЕНИЕ 2', 'Сведения об испытаниях электродвигателя', '23'),
            ('ПРИЛОЖЕНИЕ 3', 'Сведения о ремонтах электродвигателя', '24'),
        )
        rows = len(data)
        styles = [
            *[['Regular12', 'Regular', 'Regular Right']] * rows
        ]
        table_data = values(data, {})
        table = self.table(table_data, styles, [2, 7, 1])
        table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        self.Story.append(table)
        #self.Story.append(Spacer(1, 0.5 * cm))

    def page3(self):
        self.Story.append(PageBreak())
        self.formular('1 Регистрация работ')

        ptext = '<b>Фамилия И.О.</b><br/>' + '<br/>'.join(
                [Employee.objects.get_by_full_name(x['name']).fio() for x in self.data.get('team')]
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

        text = '\n'.join(['____________________' + Employee.objects.get_by_full_name(x['name']).fio() for x in self.data.get('team')])
        table2 = Table([[Paragraph(text, self.styles['Signature Left'])]])
        table2.hAlign = 'LEFT'
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
        self.Story.append(Spacer(1, 1 * cm))

    def page4(self):
        self.Story.append(PageBreak())
        template = [
            ['Список сертифицированных членов бригады'],
            [
                '№ п/п', 'Фамилия И.О.', '№ квалифика-<br/>ционного удостоверения',
                'Дата выдачи', 'Срок дейст-<br/>вия', 'Виды конт-<br/>роля', 'Уро-<br/>вень', 'Группа ЭБ'
            ]
        ]

        for num, person in enumerate(self.data.get('team'), start=1):
            emp = Employee.objects.get_by_full_name(person['name'])
            cert = Certificate.objects.get(employee=emp)
            data = [num, emp.fio(), *cert.details()]
            template.append(list(map(lambda x: str(x), data)))
        cols = len(template[0])
        rows = len(template)
        styles = [
            ['Regular Bold Center'] * cols,
            *[['Regular Center'] * cols] * (rows - 1),
        ]
        table_data = values(template, {})
        table = self.table(table_data, styles, [1, 2, 2, 1, 1, 1, 1, 1], styleTable=True)
        table.setStyle(TableStyle([
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('SPAN', (0,0), (-1, 0)),
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
        print('measurers:', self.data.get('measurers'))
        for num, measurer in enumerate(self.data.get('measurers'), start=1):
            meas = Measurer.objects.get(id=measurer)
            data = [num, *meas.details()]
            template.append(list(map(lambda x: str(x), data)))
        cols = len(template[0])
        rows = len(template)
        styles = [
            ['Regular Bold Center'] * cols,
            *[['Regular Center'] * cols] * (rows - 1),
        ]
        table_data = values(template, {})
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
            self.preetify(StaticText().get_list('normatives.txt'), 'Paragraph', 'Paragraph Justified'),
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

        data = self.data.get('engine')
        engine = Engine.objects.get(name=data.get('type'))
        engine_data = engine.details()
        random_data = engine.random_data.get('moments')

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
        rows = len(template)
        styles = [
            *[['Regular'] + ['Regular Center']] * rows
        ]
        data.update(engine_data)
        table_data = values(template, data)
        table = self.table(table_data, styles, [5, 5], styleTable=True)
        table.setStyle(TableStyle([
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('TOPPADDING', (0,0), (-1,-1), 2),
        ]))
        table.hAlign = 'LEFT'
        self.Story.append(table)
        self.Story.append(Spacer(1, 0.5 * cm))

    def page9(self):
        self.Story.append(PageBreak())
        self.formular('4 Данные заводских замеров и приёмо-сдаточных испытаний')
    
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
        self.put('Взрывозащищённый электродвигатель ' + self.data['engine']['type'], 'Regular Bold Center', 1)

        image = UploadedFile.objects.get(pk=self.data['files']['main'])
        self.put_photo(image, size=14)
        self.Story.append(Spacer(1, 1 * cm))

    def page11(self):
        self.Story.append(PageBreak())

        self.formular('6 Конструктивная схема электродвигателя')
        engine = Engine.objects.get(name=self.data['engine']['type'])
        self.put_image(engine.scheme, size=12.5)
        self.Story.append(Spacer(1, 1 * cm))

        # Until paste into report only the first connection type's picture
        self.formular('6-1 Электрическая схема подключения электродвигателя')
        self.put_image(engine.connection.all()[0].scheme)

    def page12(self):
        self.Story.append(PageBreak())

        self.formular('7 Тепловизионный контроль. Определение соответствия электродвигателя температурному классу')

        image1 = self.fetch_image(
            UploadedFile.objects.get(pk=self.data['files']['therm1']),
            size=9
        )
        image2 = self.fetch_image(
            UploadedFile.objects.get(pk=self.data['files']['therm2']),
            size=9
        )
        table_data = [[image1, image2]]
        table = Table(table_data,colWidths=self.columnize(5, 5))
        table.hAlign = 'LEFT'
        table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ]))
        self.Story.append(table)

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
        table_data = values(data, therm_data)
        table = self.table(table_data, [['Regular', 'Regular Center']] * rows, [8, 2], styleTable=True)
        self.Story.append(table)

    def page13(self):
        self.Story.append(PageBreak())

        self.formular('8 Вибрационный контроль электродвигателя')
        text = 'Среднеквадратичные значения виброскоростей  ротора в собственных опорах, мм/с'
        self.put(text, 'Regular Bold Center', 0.5)

        vibro = self.data['vibro']
        data = [
            ['Зона контроля', 'Вертикальная', 'Горизонтальная', 'Осевая'],
            ['Подшипниковый узел со стороны привода', '{vert}', '{horiz}', '{axis}'],
            ['Подшипниковый узел с противоположной приводу стороны', '{reverse_vert}', '{reverse_horiz}', '{reverse_axis}'],
            ['Норма', '{norm}', '', ''],
        ]
        styles = [
            ['Regular Bold Center'] * 4,
            *[['Regular'] + ['Regular Center'] * 3] * 3
        ]
        table_data = values(data, vibro)
        table = self.table(table_data, styles, [4, 2, 2, 2])
        table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 0.5, colors.black),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('SPAN', (1,3), (3,3))
        ]))
        self.Story.append(table)
        self.Story.append(Spacer(1, 0.5 * cm))

        data = [
            ['Зона контроля', 'Соответствие норме'],
            ['Подшипники', 'соответствует'],
            ['Установка электродвигателя на раму агрегата', 'соответствует'],
            ['Дисбаланс ротора', 'соответствует'],
        ]
        styles = [
            ['Regular Bold Center'] * 2,
            *[['Regular', 'Regular Center']] * 3
        ]
        table_data = values(data, {})
        table = self.table(table_data, styles, [5, 5])
        table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 0.5, colors.black),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]))
        self.Story.append(table)

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

        table_data = [[
            fetch_static_image('engine_details_scheme_1.jpg', 5.3),
            fetch_static_image('engine_details_scheme_2.jpg', 5.3),
            fetch_static_image('engine_details_scheme_3.jpg', 5.3),
        ]]
        table = Table(table_data) 
        table.hAlign = 'LEFT'
        self.Story.append(table)
        self.Story.append(Spacer(1, 0.5 * cm))

        engine = Engine.objects.get(name=self.data['engine']['type'])
        data = engine.random_data.get('moveable_Ex_connections')
        template = [
            ['№ п/п', 'Подвижное взрывонепроницаемое соединение', 'L1, мм', 'D, мм', 'd, мм', 'W1, мм', 'S, Ra'],
            ['1', 'Узел взрывозащиты подшипникового узла со стороны привода', '{top_point[L1]}', '{top_point[D]}', '{top_point[d]}', '{top_point[W1]}', '{top_point[S]}'],
            ['2', 'Узел взрывозащиты подшипникового узла с противоположной приводу стороны', '{bottom_point[L1]}', '{bottom_point[D]}', '{bottom_point[d]}', '{bottom_point[W1]}', '{bottom_point[S]}'],
        ]
        cols = len(template[0])
        rows = len(template)
        styles = [
            ['Regular Bold Center'] * cols,
            *[['Regular Center'] * cols] * (rows - 1)
        ]
        table_data = values(template, data)
        table = self.table(table_data, styles, [1, 4, 1, 1, 1, 1, 1])
        table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 0.5, colors.black),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 0)
        ]))
        self.Story.append(table)
        self.Story.append(Spacer(1, 0.5 * cm))

        data = engine.random_data.get('unmoveable_Ex_connections')
        template = [
            ['№ п/п', 'Неподвижное взрывонепроницаемое соединение', 'L1, мм', 'L2, мм', 'W1, мм', 'b, мм', 'a, мм', 'f, мм', 'S, Ra'],
            ['1', 'Выводное устройство &ndash; крышка', '{out_krishka[L1]}', '{out_krishka[L2]}', '{out_krishka[W1]}', '{out_krishka[b]}', '{out_krishka[a]}', '{out_krishka[f]}', '{out_krishka[S]}'],
            ['2', 'Выводное устройство &ndash; станина', '{out_stanina[L1]}', '{out_stanina[L2]}', '{out_stanina[W1]}', '{out_stanina[b]}', '{out_stanina[a]}', '{out_stanina[f]}', '{out_stanina[S]}'],
            ['3', 'Крышка узла взрывозащиты &ndash; подшипниковый щит со стороны привода', '{cap_shield[L1]}', '{cap_shield[L2]}', '{cap_shield[W1]}', '{cap_shield[b]}', '{cap_shield[a]}', '{cap_shield[f]}', '{cap_shield[S]}'],
            ['4', 'Крышка узла взрывозащиты &ndash; подшипниковый щит с противоположной приводу стороны', '{cap_shield_reverse[L1]}', '{cap_shield_reverse[L2]}', '{cap_shield_reverse[W1]}', '{cap_shield_reverse[b]}', '{cap_shield_reverse[a]}', '{cap_shield_reverse[f]}', '{cap_shield_reverse[S]}'],
        ]
        cols = len(template[0])
        rows = len(template)
        styles = [
            ['Regular Bold Center'] * cols,
            *[['Regular Center'] * cols] * (rows - 1)
        ]
        table_data = values(template, data)
        table = self.table(table_data, styles, [1, 2, 1, 1, 1, 1, 1, 1, 1])
        table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 0.5, colors.black),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 0)
        ]))
        self.Story.append(table)

        template = [
            ['Зазор между лопастями вентилятора и защитным кожухом',
            'Не менее 1/100 максимального диаметра вентилятора согласно п.17.3 ГОСТ Р 51330.0'],
            ['Наружные и внутренние контактные зажимы заземляющих проводников',
            'Обеспечивают подсоединение проводника сечением не менее 4 мм² согласно п. 15.4 ГОСТ Р 51330.0']
        ]
        cols = len(template[0])
        rows = len(template)
        styles = [['Regular'] * cols] * rows
        table_data = values(template, {})
        table = self.table(table_data, styles, [4, 6])
        table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 0.5, colors.black),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 0)
        ]))
        self.Story.append(table)

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
            *[['Regular'] * cols] * (rows - 1)
        ]
        table_data = values(template, {})
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
            *[['Regular'] * cols] * (rows - 1)
        ]
        table_data = values(template, {})
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
        table_data = values(template, {})
        table = self.table(table_data, styles, [8, 2], styleTable=True)
        table.setStyle(TableStyle([
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ('TOPPADDING', (0,0), (-1,-1), 5),
        ]))
        self.Story.append(table)


    def page17(self):
        self.Story.append(PageBreak())
        self.formular('10 Ультразвуковая дефектоскопия и толщинометрия взрывозащищённой оболочки электродвигателя')

        engine = Engine.objects.get(name=self.data['engine']['type'])
        self.put_image(engine.meters, size=12.5)
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
        table_data = values(template, zones_data)
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
        cols = len(template[0])
        rows = len(template)
        styles = [
            *[['Regular Bold Center'] * cols] * 2,
            *[['Regular'] + ['Regular Center'] * (cols - 1)] * (rows - 2),
        ]
        table_data = values(template, zones_data)
        table = self.table(table_data, styles, [3, 1, 1, 1, 2, 2], styleTable=True)
        table.setStyle(TableStyle([
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('SPAN', (0,0), (0, 1)),
            ('SPAN', (1,0), (3, 0)),
            ('SPAN', (4,0), (5, 0)),
        ]))
        self.Story.append(table)

    def page18(self):
        self.Story.append(PageBreak())
        self.formular('11 Измерение сопротивления обмотки статора постоянному току')
        self.put('Схема подключения прибора', 'Regular Center', 0.2)
        img = fetch_static_image('meter_scheme.gif', 5.3)
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
        table_data = values(template, self.data['resistance'])
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
        self.put('Упрощенная схема подключения мегаомметра', 'Regular Center', 0.2)
        img = fetch_static_image('megaommetr_scheme.jpg', 5.3)
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
        table_data = values(template, self.data['resistance'])
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

        self.put('В соответствии с требованиями нормативной документации и с результатами диагностики и исследований необходимо:', 'Paragraph Justified', 0.2)

        text = StaticText().get_list('recommendations.txt')
        data = values(text, self.data['engine'])
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

        template = StaticText().plain('decision.txt')
        cols = len(template[0])
        rows = len(template)
        styles = [
            *[['Paragraph Justified Indent'] * cols] * rows
        ]
        table_data = values(template, self.data['engine'])
        table = self.table(table_data, styles, [10])
        table.setStyle(TableStyle([
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ]))
        self.Story.append(table)

    def page21(self):
        self.Story.append(PageBreak())
        self.formular('15 Выполненные мероприятия в процессе проведения работ')

        self.put('В процессе технического диагностирования были проведены следующие мероприятия:', 'Paragraph', 0.2)
        text = StaticText().get_list('completed_tasks.txt')
        data = values(text, self.data['engine'])
        table = Table(
            self.preetify(data, 'Paragraph', 'Paragraph Justified'),
            colWidths=self.columnize(1,9)
        )
        table.hAlign = 'LEFT'
        table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        self.Story.append(table)

    def appendix(self, title, columns, widths):
        self.Story.append(PageBreak())
        self.formular(title, header='Приложение')
        template = [
            columns,
            *[list(map(lambda _: '&nbsp;', columns))] * 39
        ]
        rows = len(template)
        cols = len(template[0])
        styles = [
            *[['Regular Bold Center'] * cols] * rows
        ]
        table_data = values(template, {})
        table = self.table(table_data, styles, widths)
        table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 0.5, colors.black),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 0),
        ]))
        #table.hAlign = 'RIGHT'
        self.Story.append(table)
    '''
        Helper functions
    '''

    def table(self, data, styles, colWidths=(10, ), styleTable=False):
        table = Table(
            self.tabelize(data, styles),
            colWidths=self.columnize(*colWidths)
        )
        table.hAlign = 'LEFT'
        if styleTable:
            table.setStyle(TableStyle([
                ('BOX', (0,0), (-1,-1), 0.5, colors.black),
                ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ]))
        return table

    def tabelize(self, lst, styles=None):
        styles.reverse()
        return list(map(lambda x: self.table_row(x, styles.pop()), lst))

    def table_row(self, lst, styles):
        styles = styles or ['Regular']
        styles = styles * len(lst)
        return [Paragraph(item, self.styles[styles[n]]) for n, item in enumerate(lst)]

    def preetify(self, lst, *style):
        return list(map(
            lambda a, b: [
                Paragraph(a, self.styles[style[0]]),
                Paragraph(b, self.styles[style[1]])
            ], *zip(*lst)
            )
        )

    def formular(self, text, header='ФОРМУЛЯР'):
        table = self.table([[header + ' № ' + text]], [['Page Header']])
        table.setStyle(TableStyle([
            ('INNERGRID', (0,0), (-1,-1), 1, colors.black),
            ('BOX', (0,0), (-1,-1), 2, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('TOPPADDING', (0,0), (-1,-1), 0),
        ]))
        table.hAlign = 'LEFT'
        self.Story.append(table)
        self.Story.append(Spacer(1, 0.5 * cm))

    def columnize(self, *widths):
        return [self.full_width * width * 0.1 for width in widths]

    def mput(self, content_list, style_name, spacer=None):
        list(map(lambda x: self.put(x, style_name), content_list))

        if spacer:
            self.Story.append(Spacer(1, spacer * cm))

    def put(self, content, style_name, spacer=None):
        self.Story.append(Paragraph(content, self.styles[style_name]))

        if spacer:
            self.Story.append(Spacer(1, spacer * cm))

    ''' 
        Working with images
    '''
    def put_image(self, image, size=10):
        MEDIA_ROOT = environ.Path(settings.MEDIA_ROOT)
        ratio = float(image.width/image.height)
        image = Image(str(MEDIA_ROOT.path(str(image))),
            width=size * cm * ratio, height=size * cm)
        self.Story.append(image)

    def put_photo(self, image, size=10):
        self.Story.append(self.fetch_image(image, size))

    def fetch_image(self, image, size):
        MEDIA_ROOT = environ.Path(settings.MEDIA_ROOT)
        file_ = str(MEDIA_ROOT.path(str(image.name)))
        image = PILImage.open(file_)
        ratio = float(image.width/image.height)
        return Image(file_, width=size * cm * ratio, height=size * cm)

    '''
        Other setup utils
    '''
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
     
    def setup_page_templates(self, doc):
        frame_full = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='no_header')
        template_title = PageTemplate(id='Title', frames=frame_full)

        frame_with_header = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height-2*cm,
                bottomPadding=0, leftPadding=0, rightPadding=0, topPadding=0,
                id='with_header')
        header_content = Paragraph('''{org} {lpu} {ks} {location} {plant}
            станционный №{station_number} зав.№{serial_number}'''.format(
                **self.obj_data, **self.data['engine']
            ), self.styles["Page Header"]
        )
        template_content = PageTemplate(id='Content', frames=frame_with_header, onPage=partial(header, content=header_content))

        doc.addPageTemplates([template_title, template_content])

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
            fontSize=13,
            leading=18,
            #borderColor=colors.black,
            #borderWidth=1,
            #leftIndent=1*cm,
            alignment=TA_CENTER))
        self.styles.add(ParagraphStyle(
            name='MainTitle',
            fontName='Times Bold',
            fontSize=16,
            leading=20,
            alignment=TA_CENTER))
        self.styles.add(ParagraphStyle(
            name='Signature',
            fontName='Times',
            fontSize=13,
            leading=30,
            alignment=TA_CENTER))
        self.styles.add(ParagraphStyle(
            name='Signature Left',
            fontName='Times',
            leading=30,
            fontSize=13,
            alignment=TA_LEFT))
        self.styles.add(ParagraphStyle(
            name='Signature Handwrite',
            fontName='Times',
            fontSize=13,
            leftIndent=1*cm,
            leading=30,
            alignment=TA_CENTER))
        self.styles.add(ParagraphStyle(
            name='Page Header',
            fontName='Times Bold',
            fontSize=13,
            leading=16,
            alignment=TA_JUSTIFY))
        self.styles.add(ParagraphStyle(
            name='Regular',
            fontName='Times',
            fontSize=13,
            leading=13,
            alignment=TA_LEFT))
        self.styles.add(ParagraphStyle(
            name='Regular12',
            fontName='Times',
            fontSize=12,
            leading=13,
            alignment=TA_LEFT))
        self.styles.add(ParagraphStyle(
            name='Regular Center',
            fontName='Times',
            fontSize=13,
            leading=16,
            alignment=TA_CENTER))
        self.styles.add(ParagraphStyle(
            name='Regular Right',
            fontName='Times',
            fontSize=13,
            leading=16,
            alignment=TA_RIGHT))
        self.styles.add(ParagraphStyle(
            name='Regular Justified',
            fontName='Times',
            fontSize=13,
            leading=16,
            alignment=TA_JUSTIFY))
        self.styles.add(ParagraphStyle(
            name='Regular Bold Center',
            fontName='Times Bold',
            fontSize=13,
            alignment=TA_CENTER))
        self.styles.add(ParagraphStyle(
            name='Table Content',
            fontName='Times',
            leading=16,
            fontSize=13,
            alignment=TA_LEFT))
        self.styles.add(ParagraphStyle(
            name='Paragraph',
            fontName='Times',
            fontSize=13,
            leading=18,
            firstLineIndent=0.7 * cm,
            alignment=TA_LEFT))
        self.styles.add(ParagraphStyle(
            name='Paragraph Justified',
            fontName='Times',
            fontSize=13,
            leading=18,
            alignment=TA_JUSTIFY))
        self.styles.add(ParagraphStyle(
            name='Paragraph Justified Indent',
            fontName='Times',
            fontSize=13,
            leading=18,
            firstLineIndent=0.7 * cm,
            alignment=TA_JUSTIFY))
