from datetime import datetime
from functools import partial
from collections import defaultdict
from itertools import chain

from django.forms.models import model_to_dict
from django.db.models import Q

from reportlab.platypus import Paragraph, Image, NextPageTemplate, TableStyle, Preformatted, Table, Spacer, KeepTogether
from reportlab.platypus.doctemplate import PageTemplate
from reportlab.lib.styles import ParagraphStyle as PS
from reportlab.platypus.flowables import Flowable
from reportlab.platypus.frames import Frame
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas

from gmp.authentication.models import Employee
from gmp.certificate.models import Certificate
from gmp.inspections.models import Organization, LPU
from gmp.departments.models import Measurer
from gmp.filestorage.models import FileStorage

from .helpers import ReportMixin


class RotededText(Flowable): #TableTextRotate
    def __init__(self, text, style):
        Flowable.__init__(self)
        self.text = text
        self.height = 4 * cm
        self.style = style

    def draw(self):
        canvas = self.canv
        canvas.rotate(90)
        p = Paragraph(self.text, style=self.style)
        w, h = p.wrap(self.height, 0)
        p.drawOn(canvas, 0, 0)

class ReportContainer(ReportMixin):
    def create(self):
        self.content_top_padding = 1.4*cm
        self.appendix_top_padding = 2.4*cm

        self.format_locale_JS_dates(self.data['order'], ('date',))
        self.format_locale_JS_dates(self.data['info'], ('investigation_date',))
        self.format_JS_dates(self.data['info'], ('license_date',))
        self.data.update({'report_code': 'ГМП-{}/{}/ТО/{}'.format(
            self.data['info']['license_number'].replace('-', '/'),
            self.data['info']['license_category'],
            datetime.now().year
        )})

        self.setup_page_templates(self.doc, self.header_content(), self.colontitle_content())
        self.Story.append(NextPageTemplate('Title'))
        self.page1()
        self.Story.append(NextPageTemplate('Content'))
        self.frame_top_padding = self.content_top_padding
        self.put_toc()
        self.page2()
        self.Story.append(NextPageTemplate('Приложение А'))
        self.frame_top_padding = self.appendix_top_padding
        self.appendixA()
        self.Story.append(NextPageTemplate('Приложение Б'))
        self.appendixB()
        self.Story.append(NextPageTemplate('Приложение В'))
        self.appendixC()
        self.Story.append(NextPageTemplate('Приложение Г'))
        self.appendixD()
        self.Story.append(NextPageTemplate('Приложение Д'))
        self.appendixE()
        self.Story.append(NextPageTemplate('Приложение Е'))
        self.appendixG()
        self.Story.append(NextPageTemplate('Приложение Ж'))
        self.appendixH()
        self.Story.append(NextPageTemplate('Приложение И'))
        self.appendixI()
        self.Story.append(NextPageTemplate('Приложение К'))
        self.appendixJ()
        self.Story.append(NextPageTemplate('Приложение Л'))
        self.appendixK()

    def put_toc(self):
        self.new_page()
        self.put('СОДЕРЖАНИЕ', 'Text Simple Center Bold', 0.5)
        self.Story.append(self.toc)

    def page1(self):
        self.put_photo('adsorber_report_title.jpg', width=16)
        self.spacer(1.5)

        template = [
            ['ОТЧЕТ № {report_code}'],
            ['ПО РЕЗУЛЬТАТАМ КОМПЛЕКСНОГО ТЕХНИЧЕСКОГО ДИАГНОСТИРОВАНИЯ'],
            ['<strong>сосуда, работающего под давлением</strong>'],
            ['<strong>{device[full_desc_capital]}</strong>'],
            ['<strong>Предприятие владелец:</strong> {obj_data[org][name]}'],
            ['<strong>Место установки:</strong> филиал {obj_data[org][name]} '
                '{obj}'''],
        ]
        obj = ', '.join([self.data['obj_data']['lpu'], self.data['obj_data']['ks'], self.data['obj_data']['plant']])
        para_style = (
            ('Heading 1 Big Bold', ),
            ('Heading 1 Big Bold', ),
            ('Heading 1 Big Bold', ),
            ('Text Simple Center Leading', ),
        )
        table_style = (
            ('TOPPADDING', (0,0), (-1,2), 0),
            ('BOTTOMPADDING', (0,0), (-1,2), 0),
        )
        data = self.data.copy()
        data.update({'obj': obj})
        self.add(template, [10], self.get_style(para_style, template), table_style,
            data=data, hAlign='CENTER')

    def paragraph(self, title, file_, data={}):
        table_style = (
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        )
        para_style = (
            ('Text',),
        )
        self.add_to_toc(title, self.styles['TOC'])
        self.spacer(.1)
        template = self.static_data_plain(file_)
        self.add(template, [10], self.get_style(para_style, template), table_style,
            data=data, spacer=.2)

    def appendix(self, file_, title=None, data={}, style='Text'):
        table_style = (
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        )
        para_style = ((style,),)

        if title:
            self.add_to_toc(title, self.styles['TOC Appendix'])
            self.spacer(.4)
        template = self.static_data_plain(file_)
        self.add(template, [10], self.get_style(para_style, template), table_style,
            data=data)

    def page2(self):
        # Main content
        self.new_page()
        self.paragraph('1 Вводная часть',
            'report_container_1.txt', self.data['device'])
        self.paragraph('1.1 Основания для проведения технического диагностирования',
            'report_container_1.1.txt', self.data['info'])
        self.paragraph('1.2 Сведения об экспертной организации',
            'report_container_1.2.txt')
        self.paragraph('1.3 Состав диагностической группы',
            'report_container_1.3.txt', data=self.data)
        self.team()
        self.paragraph('2 Перечень объектов, на которые распространяется действие отчета',
            'report_container_2.txt', data=self.data)
        self.paragraph3()
        self.paragraph('4 Цель проведения технического диагностирования', 'report_container_4.txt')
        #
        self.new_page()
        self.device()
        self.paragraph6()
        self.paragraph7()

    def paragraph3(self):
        data = self.data.get('obj_data').copy()
        org_name = data['org']['name']
        org = Organization.objects.filter(name=org_name).first()
        data.update({'org': org_name, **model_to_dict(org)})
        self.paragraph('3 Данные о заказчике', 'report_container_3.txt', data=data)

    def team(self):
        self.new_page()
        # Table header
        self.put('Таблица 1.1', 'Text', .1)
        template = [
            [
                'Фамилия И.О.', 'Сведения об аттестации',
                '№ удостоверения', 'Срок действия до'
            ]
        ]
        para_style = (('Text Simple Center', ), )
        table_style = (('BOTTOMPADDING', (0,0), (-1,-1), 6), )
        self.add(template, [2, 3.3, 2.35, 2.35], self.get_style(para_style, template), 
            table_style, styleTable=True
        )

        # For each person generate separate table for ability to span 
        # certain fields
        for person in set(self.data.get('team').values()):
            emp = Employee.objects.get(pk=person)
            fio = emp.get_full_name().replace(' ', '<br />')
            cert = Certificate.objects.filter(employee=emp)
            template = [
                [fio, *c.verbose_info()] for c in cert
            ] or [
                [fio, *['Нет данных'] * 3]
            ]
            rows = len(template)
            para_style = (('Text Simple', 'Text Simple', 'Text Simple Center', 'Text Simple Center', ), )
            table_style = (
                ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                ('SPAN', (0,0), (0, rows - 1)),
            )
            self.add(template, [2, 3.3, 2.35, 2.35], self.get_style(para_style, template),
                table_style, styleTable=True
            )
        self.spacer(.5)

    def device(self):
        data = self.data['device'].copy()
        self.paragraph('5 Характеристика и назначение объекта диагностирования',
            'report_container_5.txt', data=data)
        #
        self.put('Таблица 5.1', 'Text', .1)
        data.update(self.data['obj_data'])
        template = (
            ('Параметр', 'Характеристика'),
            ('Наименование объекта экспертизы', 'Сосуд, работающий под избыточным давлением ({full_desc})'),
            ('Год изготовления', '{manufactured_year}'),
            ('Завод-изготовитель', '{factory}'),
            ('Заводской номер', '{serial_number}'),
            ('Номер чертежа', '{scheme}'),
            ('Год ввода в эксплуатацию', '{started_year}'),
            ('Место установки', '{location} {plant} {ks}, {lpu}'),
            ('Условия эксплуатации:', ''),
            ('- давление рабочее, МПа', '{p_work}'),
            ('- давление пробное, МПа', '{p_test}'),
            ('- рабочая температура среды, °С', 'От {temp_carrier_low} до {temp_carrier_high}'),
            ('- технологическая среда', '{carrier}'),
            ('Класс опасности технологической среды по ГОСТ 12.1.007-76', '{danger_class}'),
            ('Объем рабочий, м3', '{volume}'),
            ('Масса сосуда (пустого), кг', '{weight}'),
            ('Режим нагружения', '{mode}'),
            ('Основные размеры:', ''),
            ('- внутренний диаметр обечайки, мм', '{dimensions_width_ring}'),
            ('- внутренний диаметр днища, мм', '{dimensions_width_bottom}'),
            ('- высота обечайки, мм', '{dimensions_height_ring}'),
            ('- высота днища, мм', '{dimensions_height_bottom}'),
            ('- высота сосуда (общая)', '{dimensions_height_total}'),
            ('Толщина стенок (проектная), мм:', ''),
            ('- обечайка<br />- днища', '{dimensions_side_ring}<br />{dimensions_side_bottom}'),
            ('Материал (марка стали, ГОСТ):', ''),
            ('- обечайка<br />- днища', '{material_ring}<br />{material_bottom}'),
            ('Сведения о сварке:', ''),
            ('- вид<br />- материал', '{welding[name]}<br />{welding[material]}'),
            ('Контроль при изготовлении:', ''),
            ('- методы<br />- объемы', '{control[name]}<br />{control[area]}'),
        )
        para_style = (
            ('Text Simple Center Dense', 'Text Simple Center Dense'), 
            ('Text Simple Dense', 'Text Simple Dense'), 
            ('Text Simple Dense', 'Text Simple Center Dense'), 
            ('Text Simple Dense', 'Text Simple Center Dense'), 
            ('Text Simple Dense', 'Text Simple Center Dense'), 
            ('Text Simple Dense', 'Text Simple Center Dense'), 
            ('Text Simple Dense', 'Text Simple Center Dense'), 
            ('Text Simple Dense', 'Text Simple Dense'), 
            ('Text Simple Dense', 'Text Simple Center Dense'), 
        )
        table_style = (
            ('TOPPADDING', (0,0), (-1,-1), -1),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            #('SPAN', (0,11), (0,12)),
        )
        table = self.get(template, [4, 6], self.get_style(para_style, template),
            table_style, styleTable=True, data=data
        )
        self.put_one_page([table])
        #########################################
        self.new_page()
        self.put('Таблица 5.1 (продолжение)', 'Text', .1)
        data = self.data['info'].copy()
        data['info_investigation'] = data['info_investigation'].replace('\n', '<br />')
        data['info_repair'] = data['info_repair'].replace('\n', '<br />')
        data['danger_places'] = data['danger_places'].replace('\n', '<br />')

        template = (
            ('Сведения об экспертизах промышленной безопасности, осмотрах и испытаниях', '{info_investigation}'),
            ('Сведения о замене или ремонте элементов сосуда', '{info_repair}'),
            ('Места концентраций напряжений и наиболее вероятного коррозионного износа', '{danger_places}'),
        )
        para_style = (('Text Simple',), )
        table_style = (
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        )
        self.add(template, [4, 6], self.get_style(para_style, template),
            table_style, styleTable=True, data=data
        )

    def paragraph6(self):
        self.new_page()
        self.add_to_toc('6 Результаты проведенного технического диагностирования', self.styles['TOC'])
        self.put('Результаты проведённого технического диагностирования представлены в Таблице 6.1', 'Text', .1)
        self.put('Таблица 6.1', 'Text', .1)
        template = self.get_csv('report_container_6.csv')
        para_style = (
                ('Text Simple Center',),
                ('Text Simple',),
        )
        table_style = (
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        )
        self.add(template, [4, 6], self.get_style(para_style, template), table_style, 
            data=self.data['results'], styleTable=True
        )

    def paragraph7(self):
        self.new_page()
        self.paragraph('7 Заключительная часть',
            'report_container_7.1.txt', data=self.data['device'])
        template = (
            ('{condition}', ),
            ('работоспособное, неработоспособное, предельное (табл.8.9 СТО ГАЗПРОМ 2-2.3-491-2010)', ),
        )
        para_style = (
                ('Text Simple Center Bold',),
                ('Regular Center Small',),
        )
        table_style = (
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LINEBELOW', (0,0), (0,0), 0.5, colors.black),
        )
        self.add(template, [10], self.get_style(para_style, template),
            table_style, data=self.data['device'], spacer=.2
        )
        #
        template = self.static_data_plain('report_container_7.2_7.3.txt')
        para_style = (
            ('Text',),
        )
        table_style = (
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        )
        data = self.data['device'].copy()
        data.update({'report_EPB': self.data['report_code'].replace('ТО', 'ЭПБ')})
        self.add(template, [10], self.get_style(para_style, template),
            table_style, data=data, spacer=4
        )
        #
        template = [[
            '{rank}', '{fio}'
        ]]
        para_style = (
            ('Text Simple Center',),
        )
        self.add(template, [7, 3], self.get_style(para_style, template),
            table_style, data=self.data['signers']['create']
        )
    
    def appendixA(self):
        self.new_page()
        title = 'ПЕРЕЧЕНЬ ИСПОЛЬЗОВАННОЙ ПРИ ТЕХНИЧЕСКОМ ДИАГНОСТИРОВАНИИ ' \
            'НОРМАТИВНОЙ, ТЕХНИЧЕСКОЙ И МЕТОДИЧЕСКОЙ ЛИТЕРАТУРЫ'
        self.add_to_toc(title, self.styles['TOC Appendix'])
        self.spacer(1)
        template = self.static_data_list('report_container_appendixA_1.txt')
        para_style = (
            ('Text Simple Height',),
        )
        table_style = (
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        )
        self.add(template, [0.5, 9.5], self.get_style(para_style, template),
            table_style
        )

    def appendixB(self):
        self.new_page()
        text = 'СХЕМЫ ПРОВЕДЕНИЯ НЕРАЗРУШАЮЩЕГО КОНТРОЛЯ'
        title = self.add_to_toc_and_return(text, self.styles['TOC Appendix'])
        image = FileStorage.objects.get(pk=self.data['files']['legend'][0]['id'])
        image = self.get_photo(image)
        pack = [
            title,
            Spacer(0.1 * cm, 0.4 * cm),
            image
        ]
        self.put_one_page(pack)
        ####################
        self.new_page()
        image = FileStorage.objects.get(pk=self.data['files']['control_VIK'][0]['id'])
        image = self.get_photo(image)
        pack = [
            image,
            Spacer(0.1 * cm, 0.3 * cm),
            Paragraph('Рис. 1 ' + self.data['schemes']['VIK'], self.styles[ 'Text Simple Center Bold'])
        ]
        self.put_one_page(pack)
        ####################
        self.new_page()
        image = FileStorage.objects.get(pk=self.data['files']['control_UK_container'][0]['id'])
        image = self.get_photo(image)
        pack = [
            image,
            Spacer(0.1 * cm, 0.3 * cm),
            Paragraph('Рис. 2 ' + self.data['schemes']['UK_container'], self.styles[ 'Text Simple Center Bold'])
        ]
        self.put_one_page(pack)
        ####################
        self.new_page()
        image = FileStorage.objects.get(pk=self.data['files']['control_UK_connections'][0]['id'])
        image = self.get_photo(image)
        pack = [
            image,
            Spacer(0.1 * cm, 0.3 * cm),
            Paragraph('Рис. 3 ' + self.data['schemes']['UK_connections'], self.styles[ 'Text Simple Center Bold'])
        ]
        self.put_one_page(pack)
        ####################
        self.new_page()
        image = FileStorage.objects.get(pk=self.data['files']['control_magnit'][0]['id'])
        image = self.get_photo(image)
        pack = [
            image,
            Spacer(0.1 * cm, 0.3 * cm),
            Paragraph('Рис. 4 ' + self.data['schemes']['magnit'], self.styles[ 'Text Simple Center Bold'])
        ]
        self.put_one_page(pack)

    def appendixC(self):
        self.new_page()
        self.add_to_toc('Заключение по результатам визуального и измерительного контроля',
            self.styles['TOC Appendix Hidden'])
        self.appendix_header()
        self.put('ЗАКЛЮЧЕНИЕ № {}/ВИК'.format(self.data['report_code']), 'Text Simple Center Bold', .2)
        self.put('по результатам визуального и измерительного контроля', 'Text Simple Center', .5)
        self.put(self.data['info']['investigation_date'], 'Text Simple Right')
        self.put('Применяемое оборудование:', 'Text Simple Bold', .2)
        ######################################
        for measurer in Measurer.objects.filter(
                Q(id__in=self.data.get('measurers')),
                Q(name__icontains='визуальн') |
                Q(name__icontains='люксметр') |
                Q(name__icontains='дальномер')
            ):
            self.put('<bullet>&ndash;</bullet>' + measurer.verbose_info(), 'Text Simple Indent')
        ######################################
        self.put('Контроль и оценка качества элементов сосуда выполнены согласно:', 'Text Simple Bold', .2)
        self.put('РД 03-606-03; ПБ 03-584-03; СТО Газпром 2-2.3-491-2010.', 'Text Simple', .2)
        self.put('Объем контроля – см. в Приложении Б., Рис. 1', 'Text Simple', .2)
        ######################################
        self.put('Результаты визуального и измерительного контроля', 'Text Simple Center Bold', .2)
        a = enumerate(map(lambda x: x['value'], self.data['results']['VIK']['results']), start=1)
        template = tuple(map(lambda x: (str(x[0]), x[1]), a))
        para_style = (
            ('Text Simple Height',),
        )
        table_style = (
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        )
        self.add(template, [0.4, 9.6], self.get_style(para_style, template),
            table_style, spacer=1
        )
        ######################################
        self.put('<strong>Заключение: </strong>' +
            self.data['results']['VIK']['conclusion'],
            'Text', 8.2)
        self.add_specialist('Визуальный и измерительный контроль', 'ВИК')

    def appendixD(self):
        self.new_page()
        self.add_to_toc('Протокол ультразвуковой толщинометрии элементов сосуда',
            self.styles['TOC Appendix Hidden'])
        self.appendix_header()
        self.put('ПРОТОКОЛ № {}/УТ'.format(self.data['report_code']), 'Text Simple Center Bold', .2)
        self.put('ультразвуковой толщинометрии элементов сосуда', 'Text Simple Center', .5)
        self.put(self.data['info']['investigation_date'], 'Text Simple Right')
        self.put('Применяемое оборудование:', 'Text Simple Bold', .2)
        ######################################
        for measurer in Measurer.objects.filter(
                Q(id__in=self.data.get('measurers')),
                Q(name__icontains='толщиномер ультразвуковой') |
                Q(name__icontains='стандартный образец предприятия') |
                Q(name__icontains='образец шероховатости поверхности')
            ):
            self.put('<bullet>&ndash;</bullet>' + measurer.verbose_info(), 'Text Simple Indent')
        ######################################
        self.put('Контроль и оценка качества элементов сосуда выполнены согласно:', 'Text Simple Bold', .2)
        self.put('ГОСТ Р 55614-2013, РД 03-421-01, ПБ 03-584-03, СТО Газпром 2-2.3-491-2010.', 'Text Simple', .2)
        self.put('Объем контроля – см. в Приложении Б., Рис. 2', 'Text Simple', .2)
        ######################################
        self.put('Результаты контроля', 'Text Simple Center Bold', .2)
        template = (
            ('№<br />точки', 'Толщина<br />паспортная,<br />мм', 
            'Толщина<br />фактическая,<br />мм',) * 2,
        )
        data = enumerate(self.data['results']['UT']['common'], start=1)
        data = self.proc_UT_results_data(data)
        template = template + (*data,)
        para_style = (
            ('Text Simple Center Dense',),
        )
        table_style = (
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        )
        self.add(template, [1,2,2,1,2,2], self.get_style(para_style, template),
            table_style, styleTable=True
        )
        ######################################
        self.append_UT_results_data('top_bottom', 'Верхнее днище')
        self.append_UT_results_data('ring', 'Обечайка')
        self.append_UT_results_data('bottom_bottom', 'Днище нижнее')
        self.append_UT_results_data('top_cap', 'Люк верхний')
        self.append_UT_results_data('bottom_cap', 'Люк нижний')
        ######################################
        self.put('<strong>Заключение: </strong>', 'Text', .2)
        a = enumerate(map(lambda x: x['value'], self.data['results']['UT']['results']), start=1)
        template = tuple(map(lambda x: (str(x[0]), x[1]), a))
        para_style = (
            ('Text Simple Height',),
        )
        table_style = (
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        )
        self.add(template, [0.4, 9.6], self.get_style(para_style, template),
            table_style, spacer=8.2
        )
        self.add_specialist('Ультразвуковая толщинометрия элементов сосуда', 'УК')

    def appendixE(self):
        self.new_page()
        self.add_to_toc('Заключение по результатам ультразвукового контроля качества сварных соединений',
            self.styles['TOC Appendix Hidden'])
        self.appendix_header()
        self.put('ЗАКЛЮЧЕНИЕ № {}/УК'.format(self.data['report_code']), 'Text Simple Center Bold', .2)
        self.put('по результатам ультразвукового контроля качества сварных соединений', 'Text Simple Center', .5)
        self.put(self.data['info']['investigation_date'], 'Text Simple Right')
        self.put('Применяемое оборудование:', 'Text Simple Bold', .2)
        ######################################
        for measurer in Measurer.objects.filter(
                Q(id__in=self.data.get('measurers')),
                Q(name__icontains='дефектоскоп ультразвуковой') |
                Q(name__icontains='контрольный образец') |
                Q(name__icontains='образец шероховатости поверхности') |
                Q(name__icontains='люксметр') |
                Q(name__icontains='стандартный образец предприятия')
            ):
            self.put('<bullet>&ndash;</bullet>' + measurer.verbose_info(), 'Text Simple Indent')
        ######################################
        self.put('Контроль и оценка качества элементов сосуда выполнены согласно:', 'Text Simple Bold', .2)
        self.put('ГОСТ Р 55724-2013; ГОСТ Р 55809-2013; ГОСТ Р 55808-2013; СТО 00220256-005-2005;', 'Text Simple', .2)
        self.put('СТО Газпром 2-2.3-491-2010.', 'Text Simple', .2)
        self.put('Объем контроля – см. в Приложении Б., Рис. 3.', 'Text Simple', .2)
        ############################################
        # Header
        ############################################
        data = ((
            RotededText('№ участка', self.styles['Text Simple Center Dense']),
            RotededText('№ дефекта', self.styles['Text Simple Center Dense']),
            RotededText('Эквивалентная площадь дефекта, S, мм', self.styles['Text Simple Center Dense']),
            RotededText('Глубина залегания, Н,мм', self.styles['Text Simple Center Dense']),
            RotededText('Протяженность ∆L,мм', self.styles['Text Simple Center Dense']),
            RotededText('Форма (характер) дефекта (объемный/ плоскостной)', self.styles['Text Simple Center Dense']),
            RotededText('Место положение на сварном шве L, мм', self.styles['Text Simple Center Dense']),
            RotededText('Примечания', self.styles['Text Simple Center Dense']),
            RotededText('Заключение (годен, ремонт, не годен)', self.styles['Text Simple Center Dense']),
        ), )
        
        style = TableStyle([
            ('ALIGN', (0,0), (-1, -1), 'CENTER'),
            ('TOPPADDING', (0,0), (-1, -1), 10),
            ('BOTTOMPADDING', (0,0), (-1, -1), 10),
            ('LEFTPADDING', (0,0), (0, 0), 15),
            ('LEFTPADDING', (1,0), (1, 0), 15),
            ('LEFTPADDING', (2,0), (2, 0), 40),
            ('LEFTPADDING', (3,0), (3, 0), 30),
            ('LEFTPADDING', (4,0), (4, 0), 30),
            ('LEFTPADDING', (5,0), (5, 0), 60),
            ('LEFTPADDING', (6,0), (6, 0), 40),
            ('LEFTPADDING', (7,0), (7, 0), 10),
            ('LEFTPADDING', (8,0), (8, 0), 40),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ])
        
        p = Paragraph('Результаты контроля', self.styles['Text Simple Center Bold'])
        tab = Table(data, colWidths=self.columnize(.8,.6,1,1,1,1.5,1,1.6,1.5), style=style)
        ############################################
        # Data
        ############################################
        results = []
        results.extend(self.append_UT_defect('top_bottom', 'Днище верхнее'))
        results.extend(self.append_UT_defect('ring', 'Обечайка'))
        results.extend(self.append_UT_defect('bottom_bottom', 'Днище нижнее'))
        self.spacer(1)
        ######################################
        zakl = Paragraph('<strong>Заключение: </strong>' +
            self.data['results']['UK']['conclusion'], self.styles['Text'])
        self.Story.append(KeepTogether([
            p, Spacer(1 * cm, .7 * cm), tab, *results,
            Spacer(1 * cm, 1 * cm),
            zakl, Spacer(1 * cm, 5.2 * cm)
        ]))
        self.add_specialist('Ультразвуковой контроль качества сварных соединений', 'УК')

    def appendixG(self):
        self.new_page()
        self.add_to_toc('Протокол контроля физико-механических свойств (твёрдости) ' + 
            'сварных соединений и основного металла', self.styles['TOC Appendix Hidden'])
        self.appendix_header()
        self.put('ПРОТОКОЛ № {}/Т'.format(self.data['report_code']), 'Text Simple Center Bold', .2)
        self.put('контроля физико-механических свойств (твёрдости) сварных ' + 
            'соединений и<br />основного металла', 'Text Simple Center', .5)
        self.put(self.data['info']['investigation_date'], 'Text Simple Right')
        self.put('Применяемое оборудование:', 'Text Simple Bold', .2)
        ######################################
        for measurer in Measurer.objects.filter(
                Q(id__in=self.data.get('measurers')),
                Q(name__icontains='твердомер') |
                Q(name__icontains='меры твердости') |
                Q(name__icontains='образец шероховатости поверхности')
            ):
            self.put('<bullet>&ndash;</bullet>' + measurer.verbose_info(), 'Text Simple Indent')
        ######################################
        self.put('Контроль и оценка качества элементов сосуда выполнены согласно:', 'Text Simple Bold', .2)
        self.put('ГОСТ 22761-77; ГОСТ 9012-59; СТО Газпром 2-2.3-491-2010.', 'Text Simple', .2)
        self.put('Материал основных элементов сосуда – сталь марки 09Г2С;', 'Text Simple', .2)
        self.put('Твёрдость основного металла – 120÷180 HB для стали 09Г2С ' 
            '(таблица 8.6 СТО Газпром 2-2.3-491-2010).', 'Text Simple', .2)
        self.put('Объем контроля – см. в Приложении Б., Рис. 2.', 'Text Simple', .2)
        ######################################
        para_style = (
            ('Text Simple Center',),
        )
        table_style = (
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('VALIGN', (0,0), (-1,0), 'TOP'),
        )
        template = [
            ['№<br />п/п', 'Элемент<br />контроля', '№<br />точки', 'Зона контроля', 'Толщина<br />паспортная,<br />мм', 'Твердость<br />измеренная, НВ']
        ]
        for num, value in enumerate(self.data['results']['T']['values'], start=1):
            d = defaultdict(str)
            d.update(value)
            data = self.values([[str(num), '{element}', '{point}', '{zone}', '{width}', '{hardness}']], d)
            template.extend(data)

        table = self.get(template, [1, 2, 1.5, 2, 1.5, 2], self.get_style(para_style, template),
            table_style, styleTable=True
        )
        p = Paragraph('Результаты контроля', self.styles['Text Simple Center Bold'])
        self.Story.append(KeepTogether([p, Spacer(0, .7 * cm), table]))
        self.spacer(1)
        ######################################
        self.put('<strong>Заключение: </strong>', 'Text', .2)
        a = enumerate(map(lambda x: x['value'], self.data['results']['T']['results']), start=1)
        template = tuple(map(lambda x: (str(x[0]), x[1]), a))
        para_style = (
            ('Text Simple Height',),
        )
        table_style = (
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        )
        self.add(template, [0.4, 9.6], self.get_style(para_style, template),
            table_style, spacer=.5
        )
        self.add_specialist('Контроль физико-механических свойств (твёрдости) сварных' + 
            ' соединений и основного металла', 'ВИК')

    def appendixH(self):
        self.new_page()
        self.add_to_toc('Заключение по результатам магнитопорошкового контроля сварных ' + 
                'соединений и основного металла', self.styles['TOC Appendix Hidden'])
        self.appendix_header()
        self.put('ЗАКЛЮЧЕНИЕ № {}/МК'.format(self.data['report_code']), 'Text Simple Center Bold', .2)
        self.put('по результатам магнитопорошкового контроля сварных ' + 
            'соединений и основного металла', 'Text Simple Center', .5)
        self.put(self.data['info']['investigation_date'], 'Text Simple Right')
        self.put('Применяемое оборудование:', 'Text Simple Bold', .2)
        ######################################
        for measurer in Measurer.objects.filter(
                Q(id__in=self.data.get('measurers')),
                Q(name__icontains='устройство намагничивающее') |
                Q(name__icontains='магнитопорошкового контроля') |
                Q(name__icontains='магнитопорошковой дефектоскопии') |
                Q(name__icontains='образец шероховатости поверхности')
            ):
            self.put('<bullet>&ndash;</bullet>' + measurer.verbose_info(), 'Text Simple Indent')
        ######################################
        self.put('Контроль и оценка качества элементов сосуда выполнены согласно:', 'Text Simple Bold', .2)
        self.put('ГОСТ Р 55612-2013; ГОСТ 21105-87; РД 13-05-2006; ' +
            'СТО Газпром 2-2.3-218-2008; СТО Газпром 2-2.3-491-2010.', 'Text Simple', .2)
        self.put('Способ намагничивания: способ приложенного поля (СПП)', 'Text Simple', .2)
        self.put('Уровень чувствительности: Б.', 'Text Simple', .2)
        self.put('Вид намагничивания: продольный (полюсной).', 'Text Simple', .2)
        self.put('Объем контроля – см. в Приложении Б., Рис. 4.', 'Text Simple', .2)
        ######################################
        para_style = (
            ('Text Simple Center',),
            ('Text Simple', 'Text Simple Center', 'Text Simple Center', 'Text Simple Center', 'Text Simple Center'),
        )
        table_style = (
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        )
        template = [
            ['Объект контроля', 'Обозначение на схеме контроля',
	    'Участки с дефектами и их расположение',
	    'Обнаруженные дефекты (их размеры)', 'Оценка качества объекта']
        ]
        for value in self.data['results']['MK']['values']:
            if any(value.values()):
                d = defaultdict(str)
                d.update(value)
                data = self.values([['{element}', '{point}', '{zone}', '{defect}', '{summary}']], d)
                template.extend(data)

        table = self.get(template, [4, 1.5, 1.5, 1.5, 1.5], self.get_style(para_style, template),
            table_style, styleTable=True
        )
        p = Paragraph('Результаты контроля', self.styles['Text Simple Center Bold'])
        self.Story.append(KeepTogether([p, Spacer(0, .7 * cm), table]))
        self.spacer(1)
        ######################################
        self.put('<strong>Заключение: </strong>' +
            self.data['results']['MK']['conclusion'],
            'Text', 3.2)
        self.add_specialist('Магнитопорошковый контроль сварных соединений и основного металла', 'МК')

    def appendixI(self):
        self.new_page()
        self.add_to_toc('КОПИЯ АКТА ГИДРАВЛИЧЕСКОГО ИСПЫТАНИЯ', self.styles['TOC Appendix Hidden'])
        #self.put('КОПИЯ АКТА ГИДРАВЛИЧЕСКОГО ИСПЫТАНИЯ', 'Text Simple Center Bold', .2)
        #self.spacer(.4)
        #image = FileStorage.objects.get(pk=self.data['files']['hydra'][0]['id'])
        #self.put_photo(image)

        image = FileStorage.objects.get(pk=self.data['files']['hydra'][0]['id'])
        image = self.get_photo(image)
        story = [
            Paragraph('КОПИЯ АКТА ГИДРАВЛИЧЕСКОГО ИСПЫТАНИЯ', self.styles['Text Simple Center Bold']),
            Spacer(0.1 * cm, .4 * cm),
            image
        ]
        self.put_one_page(story)


    def appendixJ(self):
        self.new_page()
        self.add_to_toc('ПЕРЕЧЕНЬ СРЕДСТВ ИЗМЕРЕНИЙ И КОНТРОЛЯ, ИСПОЛЬЗОВАННЫХ В ' 
            'ПРОЦЕССЕ ПРОВЕДЕНИЯ ТЕХНИЧЕСКОГО ДИАГНОСТИРОВАНИЯ',
            self.styles['TOC Appendix Hidden'])
        self.put('ПЕРЕЧЕНЬ СРЕДСТВ ИЗМЕРЕНИЙ И КОНТРОЛЯ, ИСПОЛЬЗОВАННЫХ В ' 
            'ПРОЦЕССЕ ПРОВЕДЕНИЯ ТЕХНИЧЕСКОГО ДИАГНОСТИРОВАНИЯ', 'Text Simple Center Bold', .2)
        template = [
            ['№ п/п', 'Наименование', 'Зав. №', '№ свидетельства о поверке', 'Действительно до']
        ]
        ######################################
        for num, measurer in enumerate(Measurer.objects.filter(id__in=self.data['measurers']), start=1):
            m = [str(num)]
            if measurer.model:
                m.append(' '.join([measurer.name, measurer.model]))
            else:
                m.append(measurer.name)
            m.append(measurer.serial_number or '&ndash;')
            m.append(measurer.verification or '&ndash;')
            if measurer.expired_at:
                m.append(measurer.expired_at.strftime('%d.%m.%Y') + ' г.')
            else:
                m.append('&ndash;')
            template.append(m)
        para_style = (
            ('Text Simple Center Bold',),
            ('Text Simple Center Dense', 'Text Simple', 'Text Simple Center Dense',
                'Text Simple Center Dense',),
        )
        table_style = (
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        )
        self.add(template, [1, 4, 1.1, 1.9, 2], self.get_style(para_style, template),
            table_style, spacer=1, styleTable=True
        )

    def appendixK(self):
        self.new_page()
        self.add_to_toc('Копии разрешительной документации', self.styles['TOC Appendix Hidden'])
        first, *rest_licenses = map(lambda x: int(x['id']), self.data['files']['licenses'])
        image = FileStorage.objects.get(pk=first)
        image = self.get_photo(image)
        pack = [
            Paragraph('КОПИИ РАЗРЕШИТЕЛЬНОЙ ДОКУМЕНТАЦИИ', self.styles['Text Simple Center Bold']),
            Spacer(0.1 * cm, 0.4 * cm),
            image
        ]
        self.put_one_page(pack)

        for image in FileStorage.objects.filter(pk__in=rest_licenses):
            self.put_photo(image, height=12)
            #self.spacer(.3)

        #self.new_page()
        image = FileStorage.objects.get(pk=int(self.data['files']['warrant'][0]['id']))
        self.put_photo(image)

    ######################################
    # Helpers
    ######################################
    def append_UT_defect(self, key, name):
        para_style = (
            ('Text Simple Center',),
        )
        table_style = (
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        )
        template = ((name,),)
        tables = [self.get(template, [10], self.get_style(para_style, template),
            table_style, styleTable=True
        )]
        num = 0
        for defect in self.data['results']['UK'][key]:
            data = defaultdict(str)
            data.update(defect)
            other_keys = set(defect.keys()) - {'site'}
            if other_keys:
                num += 1
                template = (
                    ('{site}', str(num), '{area}', '{depth}', '{length}', '{type}',
                    '{position}', '{info}', '{result}'),
                )
                table = self.add(template, [.8,.6,1,1,1,1.5,1,1.6,1.5], self.get_style(para_style, template),
                    table_style, data=data, styleTable=True)
            else:
                template = ((data.get('site'), 'Дефектов не обнаружено', '', 'Годен'),)
                table = self.get(template, [.8, 6.1, 1.6, 1.5], self.get_style(para_style, template),
                    table_style, data=data, styleTable=True)
            tables.append(table)
        return tables

    def proc_UT_results_data(self, data):
        data = tuple(map(lambda x: (str(x[0]), x[1]['passport'], x[1]['real']), data))
        # If data-tuple contains odd number of tuples, add one tuple with the same length
        if len(data) % 2 != 0:
            data = (*data, ('',) * len(data[0]))
        a = tuple(zip(data[::2], data[1::2])) or data
        b = tuple(map(lambda x: tuple(chain.from_iterable(x)), a))
        return b

    def append_UT_results_data(self, group, header):
        data = enumerate(self.data['results']['UT'][group], start=1)
        if data:
            return
        data = self.proc_UT_results_data(data)
        template = ((header,), ) + (*data,)
        para_style = (
            ('Text Simple Center Dense',),
        )
        table_style = (
            ('SPAN', (0,0), (-1,0)),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        )
        self.add(template, [1,2,2,1,2,2], self.get_style(para_style, template),
            table_style, styleTable=True
        )

    def add_specialist(self, category, abbr):
        person_id = self.data['team'][category]
        emp = Employee.objects.get(pk=person_id)
        template = (
            (emp.get_cert_details(abbr), emp.fio(), ),
        )
        para_style = (
            ('Text Simple','Text Simple Right'),
        )
        table_style = (
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
        )
        self.add(template, [5, 5], self.get_style(para_style, template),
            table_style)

    def appendix_header(self):
        data = self.data.copy()
        data['device']['name'] = data['device']['name'].capitalize()
        template = [
            ['ООО «ГАЗМАШПРОЕКТ»', '', '{obj_data[org][name]}'],
            ['(предприятие-исполнитель)', '', '(предприятие-Заказчик)'],
            ['г. Москва, ул. Нагатинская, д. 5', '', '{obj_data[lpu]},'
                '<br />{obj_data[ks]}, {obj_data[plant]}'],
            ['(место осуществления лицензируемого вида деятельности)', '', '(место нахождения оборудования)'],
            ['', '', '{device[name]}'],
            ['', '', '(тип и наименование оборудования)'],
            ['', '', 'зав. № {device[serial_number]}, рег. № {device[reg_number]},'
                        '<br />инв. № {device[inv_number]}'],
            ['', '', '(номер оборудования)'],
        ]
        para_style = (
            ('Regular Center Italic',),
            ('Regular Center Italic Small',),
            ('Regular Center Italic',),
            ('Regular Center Italic Small',),
            ('Regular Center Italic',),
            ('Regular Center Italic Small',),
            ('Regular Center Italic',),
            ('Regular Center Italic Small',),
        )
        table_style = (
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,0), -10),
            ('LINEBELOW', (0,0), (0,0), .5, colors.black),
            ('LINEBELOW', (-1,0), (-1,0), .5, colors.black),
            ('LINEBELOW', (0,2), (0,2), .5, colors.black),
            ('LINEBELOW', (-1,2), (-1,2), .5, colors.black),
            ('LINEBELOW', (-1,4), (-1,4), .5, colors.black),
            ('LINEBELOW', (-1,6), (-1,6), .5, colors.black),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,1), (-1,1), 16),
            ('BOTTOMPADDING', (0,3), (-1,3), 16),
            ('BOTTOMPADDING', (0,5), (-1,5), 16),
            ('VALIGN', (0,0), (-1,0), 'BOTTOM'),
            ('VALIGN', (0,1), (-1,1), 'TOP'),
            ('VALIGN', (0,2), (-1,2), 'BOTTOM'),
            ('VALIGN', (0,3), (-1,3), 'TOP'),
            ('VALIGN', (0,4), (-1,4), 'BOTTOM'),
            ('VALIGN', (0,5), (-1,5), 'TOP'),
            ('VALIGN', (0,6), (-1,6), 'BOTTOM'),
            ('VALIGN', (0,7), (-1,7), 'TOP'),
        )
        self.add(template, [4, 2, 4], self.get_style(para_style, template),
            table_style, data=data, spacer=.7
        )

    # Define report's static content
    def setup_page_templates(self, doc, header_content, colontitle_content):
        frame_with_header = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
            bottomPadding=0, leftPadding=0, rightPadding=0, topPadding=0, id='with_header')
        template_title = PageTemplate(id='Title', frames=frame_with_header, onPage=partial(self.header, content=header_content))

        frame_full = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
            bottomPadding=1 * cm, leftPadding=0, rightPadding=0, topPadding=self.content_top_padding, id='no_header')
        template_content = PageTemplate(id='Content', frames=frame_full, onPage=partial(self.colontitle, content=colontitle_content))

        doc.addPageTemplates([template_title, template_content])

        frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
            bottomPadding=0, leftPadding=0, rightPadding=0, topPadding=self.appendix_top_padding, id='appendix_header')
        letters = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'И', 'К', 'Л']
        template_appendix = []
        for letter in letters:
            name = 'Приложение ' + letter
            p = Paragraph(name, self.styles['Text Simple Right']),
            content = colontitle_content + p
            template_appendix.append(PageTemplate(id=name, frames=frame, onPage=partial(self.colontitle, content=content)))
        doc.addPageTemplates(template_appendix)


    @staticmethod
    def header(canvas, doc, content):
        canvas.saveState()
        w, h = content[0].wrap(doc.width, doc.topMargin)
        content[0].drawOn(canvas, doc.width - w, 140)

        w, h = content[1].wrap(doc.width, doc.topMargin)
        content[1].drawOn(canvas, 0, h - 20)
        canvas.restoreState()


    @staticmethod
    def colontitle(canvas, doc, content):
        canvas.saveState()
        # Put page number
        style = PS(
            'Page Number',
            fontName='Times',
            fontSize=13)
        pageNumber = Paragraph(str(canvas.getPageNumber()), style=style)
        w, h = pageNumber.wrap(doc.width, doc.topMargin)
        pageNumber.drawOn(canvas, doc.width + doc.leftMargin, h + 20)

        # Put other provided content
        w, h = content[0].wrap(doc.width, doc.topMargin)
        content[0].drawOn(canvas, doc.leftMargin, doc.height)

        w, h = content[1].wrap(doc.width, doc.topMargin)
        content[1].drawOn(canvas, doc.leftMargin, doc.height)

        if len(content) == 3:
            w, h = content[2].wrap(doc.width, doc.topMargin)
            content[2].drawOn(canvas, doc.leftMargin, doc.height - 25)

        canvas.restoreState()

    def header_content(self):
        fio_string = '{fio:_>25}'
        date_string = '"___"{:_>15}'.format('_') + '{} г.'.format(datetime.now().year)
        template = [
            ['','Директор филиала<br/>ООО «ГАЗМАШПРОЕКТ» «НАГАТИНСКИЙ»'],
            ['',fio_string.format(fio='Р.Ю. Ерин')],
            ['',date_string],
            ['','М.П.']
        ]
        rows = len(template)
        styles = [
            *[['Text Simple Leading']] * rows,
        ]
        table_data = self.values(template, {})
        table = self.table(table_data, styles, [6,4], styleTable=False)
        table.hAlign = 'RIGHT'
        table.setStyle(TableStyle([
            ('TOPPADDING', (0,-1), (-1,-1), 25),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ]))

        template = [
            ['','Москва',''],
            ['','{} г.'.format(datetime.now().year),''],
        ]
        rows = len(template)
        styles = [
            *[['Text Simple Leading Center']] * rows,
        ]
        table_data = self.values(template, {})
        table2 = self.table(table_data, styles, [5.5,2,1], styleTable=False)
        return (
            table,
            table2
        )


    def colontitle_content(self):
        return (
            Paragraph('ООО «ГАЗМАШПРОЕКТ»', self.styles['Text Simple']),
            Paragraph('Отчет № {}'.format(self.data['report_code']), self.styles['Text Simple Right'])
        )
