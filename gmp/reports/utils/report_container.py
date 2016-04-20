from datetime import datetime
from functools import partial
from itertools import chain

from django.forms.models import model_to_dict

from reportlab.platypus import Paragraph, Image, NextPageTemplate, TableStyle, KeepTogether, Preformatted, Table
from reportlab.platypus.frames import Frame
from reportlab.platypus.doctemplate import PageTemplate
from reportlab.lib.units import cm
from reportlab.lib import colors

from gmp.authentication.models import Employee
from gmp.certificate.models import Certificate
from gmp.inspections.models import Organization, LPU
from gmp.departments.models import Measurer
from gmp.filestorage.models import FileStorage

from .helpers import ReportMixin


class ReportContainer(ReportMixin):
    def create(self):
        self.setup_page_templates(self.doc, self.header_content(), self.colontitle_content())

        self.format_locale_JS_dates(self.data['order'], ('date',))

        self.Story.append(NextPageTemplate('Title'))
        self.page1()
        self.Story.append(NextPageTemplate('Content'))
        self.put_toc()
        self.page2()

    def put_toc(self):
        self.new_page()
        self.put('СОДЕРЖАНИЕ', 'Regular Bold Center', 0.5)
        self.Story.append(self.toc)

    def page1(self):
        self.put_photo('adsorber_report_title.jpg', width=16)
        self.spacer(1.5)

        template = [
            ['ОТЧЕТ № ГМП-16ДИА/0012/С2/ТО/2016'],
            ['ПО РЕЗУЛЬТАТАМ КОМПЛЕКСНОГО ТЕХНИЧЕСКОГО'],
            ['ДИАГНОСТИРОВАНИЯ'],
            ['<strong>сосуда, работающего под давлением</strong>'],
            ['<strong>{device[full_desc_capital]}</strong>'],
            ['<strong>Предприятие владелец:</strong> {obj_data[org]}'],
            ['<strong>Место установки:</strong> филиал {obj_data[org]} '
                '{obj_data[lpu]} {obj_data[ks]} {obj_data[plant]}'''],
        ]
        para_style = (
            ('Heading 1 Bold', ),
            ('Heading 1 Bold', ),
            ('Heading 1 Bold', ),
            ('Regular Center Leading', ),
        )
        table_style = (
            ('BOTTOMPADDING', (0,0), (-1,2), 10),
        )
        self.add(template, [8], self.get_style(para_style, template), table_style,
            data=self.data, hAlign='CENTER')

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
        para_style = (
            (style,),
        )
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
        self.appendixA()
        self.appendixB()

    def paragraph3(self):
        data = self.data.get('obj_data').copy()
        org = Organization.objects.filter(name=data['org']).first()
        data.update({'org': data['org'].split('"')[1], **model_to_dict(org)})
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
        for person in self.data.get('team'):
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
        self.add(template, [4, 6], self.get_style(para_style, template),
            table_style, styleTable=True, data=data
        )

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
        self.add(template, [4, 6], self.get_style(para_style, template),
            table_style, styleTable=True
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
                ('Regular Bold Center',),
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
        self.add(template, [10], self.get_style(para_style, template),
            table_style, data=self.data['device'], spacer=4
        )
        #
        template = [[
            '{rank}', '{fio}'
        ]]
        para_style = (
            ('Regular Center',),
        )
        self.add(template, [7, 3], self.get_style(para_style, template),
            table_style, data=self.data['signers']['create']
        )
    
    def appendixA(self):
        self.new_page()
        self.put('Приложение А', 'Regular Right', .4)
        #self.appendix('report_container_appendixA_1.txt', style='Text Simple Height',
        #    title='ПЕРЕЧЕНЬ ИСПОЛЬЗОВАННОЙ ПРИ ТЕХНИЧЕСКОМ ДИАГНОСТИРОВАНИИ '
        #    'НОРМАТИВНОЙ, ТЕХНИЧЕСКОЙ И МЕТОДИЧЕСКОЙ ЛИТЕРАТУРЫ')
        title = 'ПЕРЕЧЕНЬ ИСПОЛЬЗОВАННОЙ ПРИ ТЕХНИЧЕСКОМ ДИАГНОСТИРОВАНИИ ' \
            'НОРМАТИВНОЙ, ТЕХНИЧЕСКОЙ И МЕТОДИЧЕСКОЙ ЛИТЕРАТУРЫ'
        self.add_to_toc(title, self.styles['TOC Appendix'])
        self.spacer(.4)
        template = self.get_csv('report_container_appendixA_1.txt')
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
        self.new_page()
        self.put('Приложение А', 'Regular Right', .4)
        template = self.get_csv('report_container_appendixA_2.txt')
        self.add(template, [0.5, 9.5], self.get_style(para_style, template),
            table_style
        )

    def appendixB(self):
        self.new_page()
        self.put('Приложение Б', 'Regular Right', .4)
        title = 'СХЕМЫ ПРОВЕДЕНИЯ НЕРАЗРУШАЮЩЕГО КОНТРОЛЯ'
        self.add_to_toc(title, self.styles['TOC Appendix'])
        self.spacer(.4)

    # Define report's static content
    def setup_page_templates(self, doc, header_content, colontitle_content):
        frame_with_header = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
                bottomPadding=0, leftPadding=0, rightPadding=0, topPadding=0,
                id='with_header')
        template_title = PageTemplate(id='Title', frames=frame_with_header, onPage=partial(self.header, content=header_content))

        frame_full = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
                bottomPadding=0, leftPadding=0, rightPadding=0, topPadding=20,
                id='no_header')
        template_content = PageTemplate(id='Content', frames=frame_full, onPage=partial(self.colontitle, content=colontitle_content))

        doc.addPageTemplates([template_title, template_content])

    @staticmethod
    def header(canvas, doc, content):
        canvas.saveState()
        w, h = content[0].wrap(doc.width, doc.topMargin)
        content[0].drawOn(canvas, doc.width - w, 120)

        w, h = content[1].wrap(doc.width, doc.topMargin)
        content[1].drawOn(canvas, 0, h - 20)
        canvas.restoreState()

    @staticmethod
    def colontitle(canvas, doc, content):
        canvas.saveState()
        w, h = content[0].wrap(doc.width, doc.topMargin)
        content[0].drawOn(canvas, doc.leftMargin, doc.height)

        w, h = content[1].wrap(doc.width, doc.topMargin)
        content[1].drawOn(canvas, doc.rightMargin, doc.height)
        canvas.restoreState()

    def header_content(self):
        date_string = '"____"{:_>21}'.format('_') + '201&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;г'
        fio_string = '{fio:_>32}'
        template = [
            ['Директор филиала<br/>ООО «ГАЗМАШПРОЕКТ» «НАГАТИНСКИЙ»'],
            [fio_string.format(fio='А.Н. Бондаренко')],
            [date_string],
            ['М.П.']
        ]
        rows = len(template)
        styles = [
            *[['Signature Left']] * rows,
        ]
        table_data = self.values(template, {})
        table = self.table(table_data, styles, [4], styleTable=False)
        table.hAlign = 'RIGHT'
        table.setStyle(TableStyle([
            ('TOPPADDING', (0,-1), (-1,-1), 25),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ]))

        template = [
            ['Москва'],
            ['{} г.'.format(datetime.now().year)],
        ]
        rows = len(template)
        styles = [
            *[['Regular Center']] * rows,
        ]
        table_data = self.values(template, {})
        table2 = self.table(table_data, styles, [11], styleTable=False)
        return (
            table,
            table2
        )


    def colontitle_content(self):
        return (
            Paragraph('ООО «ГАЗМАШПРОЕКТ»', self.styles['Regular']),
            Paragraph('Отчет № ГМП-16ДИА/0012/С2/ТО/2016', self.styles['Regular Right']),
        )

