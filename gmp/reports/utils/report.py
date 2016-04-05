from datetime import datetime
from functools import partial
from itertools import chain

from django.forms.models import model_to_dict

from reportlab.platypus import Paragraph, Spacer, Image, NextPageTemplate, TableStyle, KeepTogether
from reportlab.platypus.doctemplate import BaseDocTemplate
from reportlab.platypus.frames import Frame
from reportlab.platypus.doctemplate import PageTemplate
from reportlab.lib.units import cm
from reportlab.lib import colors

from gmp.authentication.models import Employee
from gmp.certificate.models import Certificate
from gmp.inspections.models import Organization, LPU
from gmp.departments.models import Measurer
from gmp.engines.models import Engine, ThermClass
from gmp.filestorage.models import UploadedFile

from .helpers import ReportMixin


class Report(ReportMixin):
    def create(self):
        self.setup_page_templates(self.doc, self.header_content())

        self.format_JS_dates(self.data, ('workBegin', 'workEnd'))
        self.format_JS_dates(self.data['order'], ('date',))

        self.Story.append(NextPageTemplate('Title'))
        self.page1()
        self.Story.append(NextPageTemplate('Content'))
        self.page2()
        self.page3()
        self.appendix1()
        self.appendix2()
        #self.page5_6()
        #self.page7()
        #self.page8()
        #self.page9()
        #self.page10()
        #self.page11()
        #self.page12()
        #self.page13()
        #self.page14()
        #self.page15()
        #self.page16()
        #self.page17()
        #self.page18()
        #self.page19()
        #self.page20()
        #self.page21()
        #self.appendix('1 Сведения об эксплуатации электродвигателя',
        #    ['Дата', 'Число пусков', 'Суммарная наработка, час'],
        #    [2, 3, 5])
        #self.appendix('2 Сведения об испытаниях электродвигателя',
        #    ['Дата', 'Вид', 'Содержание', 'Заключение'],
        #    [1, 2, 3, 4])
        #self.appendix('3 Сведения о ремонтах электродвигателя',
        #    ['Дата', 'Вид', 'Содержание', 'Заключение'],
        #    [1, 2, 3, 4])
        #    

    def page1(self):
        img = self.fetch_static_image('zakl_header_img.jpg', 2.3)
        img.hAlign = 'CENTER'
        self.Story.append(img)
        self.Story.append(Spacer(1, 6 * cm))

        template = [
            ['ЗАКЛЮЧЕНИЕ № 1-2/1715-10-14'],
            ['''ЭКСПЕРТИЗЫ ПРОМЫШЛЕННОЙ БЕЗОПАСНОСТИ НА ТЕХНИЧЕСКОЕ УСТРОЙСТВО,
                ЭКСПЛУАТИРУЕМОЕ НА ОПАСНОМ ПРОИЗВОДСТВЕННОМ ОБЪЕКТЕ'''],
            ['<strong>Объект:</strong> Взрывозащищённый электродвигатель {engine[type]}'],
            ['станционный № {engine[station_number]} зав.№ {engine[serial_number]}'],
            ['<strong>Владелец:</strong> {obj_data[org]}'],
            ['''<strong>Место установки:</strong> {obj_data[lpu]}, {obj_data[ks]},
                {obj_data[plant]}, {obj_data[location]}'''],
            ['№_____________________________________']
        ]
        rows = len(template)
        para_style = [
            *[['Heading 1 Bold']] * 2,
            *[['Regular Center']] * (rows - 2),
        ]
        table_style = (('BOTTOMPADDING', (0,0), (-1,-1), 10), )
        self.add(template, [8], para_style, table_style,
            data=self.data, hAlign='CENTER')

    def page2(self):
        # Main content
        self.new_page()
        self.put('Содержание', 'Regular Bold Center', 0.5)
        csv_data = self.get_csv('report_TOC.csv')
        template = csv_data[:9]
        rows = len(template)
        para_style = [
            *[['Regular Bold Center', 'Regular Justified Bold', 'Regular Right Bold']] * rows
        ]
        table_style = (
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        )
        self.add(template, [1, 8, 1], para_style, table_style)

        # Appendix content
        template = csv_data[9:]
        rows = len(template)
        para_style = [
            *[['Regular Bold Center', 'Regular Justified', 'Regular Right Bold']] * rows
        ]
        self.add(template, [2, 7, 1], para_style, table_style)

    def page3(self):
        self.new_page()
        table_style = (
            ('BOTTOMPADDING', (0,1), (-1,1), 10),
            ('BOTTOMPADDING', (0,0), (-1,0), 10),
            ('BOTTOMPADDING', (0,2), (-1,-2), 0),
            ('BOTTOMPADDING', (0,-1), (-1,-1), 10),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        )
        para_style_full = (
            ('Regular Center', 'Regular Center'),
            ('Regular Center', 'Regular Justified'),
        )
        para_style = (('Regular Center', 'Regular Justified'), )
        # 1, 1.1
        template = self.get_csv('report_main_content11.csv')
        self.add(template, [1, 9], self.get_style(para_style_full, template), table_style,
            data=self.data['info']
        )

        # 1.2
        template = self.get_csv('report_main_content12.csv')
        self.add(template, [1, 9], self.get_style(para_style, template), table_style[1:])

        # 1.3
        template = self.get_csv('report_main_content13.csv')
        self.add(template, [1, 9], self.get_style(para_style, template), table_style[1:],
            data=self.data['order'], spacer=0.5)

        ## 2
        template = self.get_csv('report_main_content2.csv')
        self.add(template, [1, 9], self.get_style(para_style_full, template), table_style[1:],
            data=self.data, spacer=0.5)

        ## 3
        template = self.get_csv('report_main_content3.csv')
        org_name = self.data['obj_data']['org']
        org = Organization.objects.get(name=org_name)
        self.add(template, [1, 9], self.get_style(para_style_full, template), table_style[1:],
            data=model_to_dict(org), spacer=0.5)

        ## 4
        template = self.get_csv('report_main_content4.csv')
        self.add(template, [1, 9], self.get_style(para_style_full, template), table_style[1:],
            data=self.data['engine'], spacer=0.5)

        ### 5
        template = self.get_csv('report_main_content5.csv')
        chapter_number = int(''.join(filter(lambda x: x.isdigit(), template[0][0])))

        docs = enumerate(filter(lambda x: x, self.data['docs']), start=1)
        docs_with_chapter_prepended = list(map(lambda x: [
            '{}.{}'.format(chapter_number, x[0]), x[1]
        ], docs))
        template.extend(docs_with_chapter_prepended)
        self.add(template, [1, 9], self.get_style(para_style_full, template), table_style[1:],
            spacer=0.5)

        ### 6
        template = self.get_csv('report_main_content6.csv')
        chapter_number = int(''.join(filter(lambda x: x.isdigit(), template[0][0])))

        docs = enumerate(filter(lambda x: x, self.data['obj_data']['detail_info']), start=1)
        docs_with_chapter_prepended = list(map(lambda x: [
            '{}.{}'.format(chapter_number, x[0]), x[1]
        ], docs))
        template.extend(docs_with_chapter_prepended)
        self.add(template, [1, 9], self.get_style(para_style_full, template), table_style[1:],
            spacer=0.5)

        ## 7
        template = self.get_csv('report_main_content7.csv')
        self.add(template, [1, 9], self.get_style(para_style_full, template), table_style[1:],
            spacer=0.5)

        ## 8
        template = self.get_csv('report_main_content8.csv')
        self.add(template, [1, 9], self.get_style(para_style_full, template), table_style[1:],
            data=self.data, spacer=0.5)

        ## 9
        template = self.get_csv('report_main_content9.csv')
        first_N_rows = template[:-1]
        self.add(first_N_rows, [1, 9], self.get_style(para_style_full, first_N_rows), table_style[1:],
            data=self.data, spacer=0.5)

        table_style = ()
        para_style = (('Regular', 'Regular Right'), )
        last_row = template[-1:]
        self.add(last_row, [5, 5], self.get_style(para_style, last_row), table_style)

    def appendix1(self):
        self.new_page()
        table_style = (
            ('BOTTOMPADDING', (0,0), (-1,0), 10),
            ('BOTTOMPADDING', (0,1), (-1,1), 20),
            ('BOTTOMPADDING', (0,2), (-1,-1), 0),
            ('BOTTOMPADDING', (0,-1), (-1,-1), 10),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('SPAN', (0,0), (-1,0)),
            ('SPAN', (0,1), (-1,1)),
        )
        para_style_full = (
            ('Regular Right Italic',),
            ('Regular Bold Center',),
            ('Regular Center', 'Regular Justified',),
        )
        para_style = (('Regular Center', 'Regular Justified'), )
        template = self.static_data_plain('report_appendix1.txt')
        numbered_list = enumerate(chain.from_iterable(template[2:]), start=1)
        stringified_numbered_list = list(map(lambda x: [str(x[0]), x[1]], numbered_list))
        template = template[:2] + stringified_numbered_list
        self.add(template, [1,9], self.get_style(para_style_full, template), table_style)

    def appendix2(self):
        self.new_page()

        self.put('Приложение 2', 'Regular Right Italic')

        for img_id in self.data['files']['main']:
            image = UploadedFile.objects.get(pk=img_id)
            self.put_photo(image, size=14)
            #print(image)
            #table_data = ((image, ))
            #table = Table(table_data, colWidths=self.columnize(5, 5))
            #table.hAlign = 'LEFT'
            #table.setStyle(TableStyle([
            #    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            #    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            #]))
            #self.Story.append(table)

    # Define report's static content
    def setup_page_templates(self, doc, header_content):
        frame_with_header = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
                bottomPadding=0, leftPadding=0, rightPadding=0, topPadding=0,
                id='with_header')
        template_title = PageTemplate(id='Title', frames=frame_with_header, onPage=partial(self.header, content=header_content))

        frame_full = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='no_header')
        template_content = PageTemplate(id='Content', frames=frame_full)

        doc.addPageTemplates([template_title, template_content])

    @staticmethod
    def header(canvas, doc, content):
        canvas.saveState()
        w, h = content[0].wrap(doc.width, doc.topMargin)
        content[0].drawOn(canvas, doc.width - w, 120)

        w, h = content[1].wrap(doc.width, doc.topMargin)
        content[1].drawOn(canvas, (doc.width) / 2, h + 30)
        canvas.restoreState()

    def header_content(self):
        date_string = '"____"{:_>21}'.format('_') + '201&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;г'
        fio_string = '{fio:_>32}'
        template = [
            ['Директор филиала<br/>ООО «ГАЗМАШПРОЕКТ» «НАГАТИНСКИЙ»'],
            [fio_string.format(fio='А.Н. Бондаренко')],
            [date_string]   
        ]
        rows = len(template)
        styles = [
            *[['Regular Center']] * rows,
        ]
        table_data = self.values(template, {})
        table = self.table(table_data, styles, [4], styleTable=False)
        table.hAlign = 'RIGHT'
        table.setStyle(TableStyle([
            ('BOTTOMPADDING', (0,0), (-1,-1), 15),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ]))
        return (
            table,
            Paragraph('{} г.'.format(datetime.now().year), self.styles['Regular'])
        )

