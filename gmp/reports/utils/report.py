from datetime import datetime
from functools import partial
from itertools import chain

from django.forms.models import model_to_dict

from reportlab.platypus import Paragraph, Image, NextPageTemplate, TableStyle, KeepTogether, Preformatted, Table
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
        self.appendix3()
        self.appendix4()

    def page1(self):
        self.put_photo('zakl_header_img.jpg')
        self.spacer(6)

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

        self.put('Приложение 2', 'Regular Right Italic', 0.5)

        for img_id in self.data['files']['main']:
            image = UploadedFile.objects.get(pk=img_id)
            self.put_photo(image)
            self.spacer(0.5)

    def appendix3(self):
        self.new_page()
        data = self.data.get('engine')
        engine = Engine.objects.get(name=data.get('type'))
        engine_data = engine.details()
        random_data = engine.random_data.get('moments')

        self.put('Приложение 3', 'Regular Right Italic', 0.5)
        self.put('Технические данные объекта', 'Regular Bold Center', 1)

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
        data.update(engine_data)
        self.add(template, [5, 5], self.get_style(para_style, template), table_style,
            data=data, styleTable=True
        )

    def appendix4(self):
        self.new_page()
        table_style = (
            ('TOPPADDING', (-1,3), (-1,3), 15),
            ('TOPPADDING', (-1,5), (-1,5), 15),
            ('TOPPADDING', (-1,5), (-1,5), 15),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,-2), (-1,-1), 0),
        )
        para_style = [
            *[['Regular Bold Center', ]] * 5, ['Regular', ],
        ]
        data = self.data
        data.update({'control_type': 'визуального и измерительного контроля'})
        template = self.static_data_plain('report_appendix_protocol_title.txt')
        self.add(template, [10], self.get_style(para_style, template), table_style,
            data=data, spacer=.15
        )

        # Measurers table
        template = [
            [
                '№<br/>п/п', 'Тип прибора', 'Заводской номер<br/>прибора',
                'Свидетельство о<br/>поверке', 'Дата следующей<br/>поверки' 
            ]
        ]
        all_measurers = Measurer.objects.filter(
            id__in=self.data.get('measurers')
        ).filter(
            name__icontains='визуальн'
        )
        for num, measurer in enumerate(all_measurers, start=1):
            template.append([str(num), *measurer.details()])
        table_style = ()
        para_style = (('Regular Center', ),)
        self.add(template, [1, 3, 2, 2, 2], self.get_style(para_style, template), table_style,
            styleTable=True, spacer=.5
        )
        
        # Headers
        res = '<u>{}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{}:</u>'.format(
            ' '.join('Результаты').upper(),
            ' '.join('контроля').upper(),
        )
        self.put(res, 'Regular Bold Center', 0.1)
        res = 'КОНТРОЛЬ ПАРАМЕТРОВ ВЗРЫВОЗАЩИТЫ'
        self.put(res, 'Regular Center', 0.2)

        # Measure data
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
            styleTable=True, spacer=.5
        )

        #
        res = 'ВИК УЗЛОВ ВЗРЫВОЗАЩИТЫ'
        self.put(res, 'Regular Bold', 0.5)
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
            ['Наличие повреждений уплотнительного кольца кабельного ввода', 'нет'],
        ]
        para_style = (('Regular', 'Regular Center'),)
        table_style = (
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('TOPPADDING', (0,0), (-1,-1), 0),
        )
        self.add(template, [8, 2], self.get_style(para_style, template), table_style,
            styleTable=True
        )
        template = [
            ['ВИК СТАТОРА', ''],                                
            ['Наличие пыли, масла, механических повреждений на корпусе статора', 'нет'],
            ['ВИК РОТОРА', ''],
            ['Коррозия и механические повреждения на наружных поверхностях деталей подшипников качения', 'нет'],
            ['Свободное вращение ротора в собранном двигателе от руки', 'да']
        ]
        para_style = (
            ('Regular Bold', ),
            ('Regular', 'Regular Center'),
            ('Regular Bold', ),
            ('Regular', 'Regular Center'),
        )
        table_style = table_style + (
            ('BOTTOMPADDING', (0,0), (0,0), 0),
            ('BOTTOMPADDING', (0,2), (0,2), 0),
            ('SPAN', (0,0), (-1,0)),
            ('SPAN', (0,2), (-1,2)),
        )
        self.add(template, [8, 2], self.get_style(para_style, template), table_style,
            styleTable=True
        )

        # VIK result
        template = [
            ['Заключение: Соответствует. Двигатель годен к дальнейшей эксплуатации без ограничений.'],
            ['Контроль провел', '{fio}'],
            ['Удостоверение № {serial_number}, '
             'выдано {received} г., '
             'действительно по {expired} г.', '']
        ]
        para_style = (
            ('Zakluchenie', ),
            ('Regular Bold', 'Regular Right Bold'),
            ('Regular Center Italic', ),
        )
        table_style = table_style + (
            ('SPAN', (0,0), (-1,0)),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ('TOPPADDING', (0,-1), (-1,-1), 10),
            ('ALIGN', (-1,1), (-1,1), 'RIGHT')
        )

        person = self.data.get('team')['VIK']
        emp = Employee.objects.get_by_full_name(person)
        cert = emp.get_certs_by_abbr('ВИК')[0]
        self.add(template, [5,5], self.get_style(para_style, template), table_style,
            data=cert.info()
        )

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

