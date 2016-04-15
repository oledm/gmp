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
        #self.styles.add(PS(
        #    name='Paragraph Justified',
        #    fontName='Times',
        #    fontSize=13,
        #    leading=18,
        #    firstLineIndent=0.7 * cm,
        #    alignment=TA_JUSTIFY))

        self.setup_page_templates(self.doc, self.header_content(), self.colontitle_content())

        #self.format_JS_dates(self.data, ('workBegin', 'workEnd'))
        self.format_locale_JS_dates(self.data['order'], ('date',))

        self.Story.append(NextPageTemplate('Title'))
        #self.new_page()
        self.page1()
        self.Story.append(NextPageTemplate('Content'))
        self.put_toc()
        self.page2()
        #self.page3()
        #self.appendix1()
        #self.appendix2()
        #self.appendix3()
        #self.appendix4()
        #self.appendix5_6()
        #self.appendix7()
        #self.appendix8()
        #self.appendix9()
        #self.appendix10()
        #self.appendix11()

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

    def paragraph(self, title, content, data={}):
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
        template = self.static_data_plain(content)
        self.add(template, [10], self.get_style(para_style, template), table_style,
            data=data, spacer=.2)

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
            ('Regular Center', 'Regular Center'), 
            ('Regular', 'Regular'), 
            ('Regular', 'Regular Center'), 
            ('Regular', 'Regular Center'), 
            ('Regular', 'Regular Center'), 
            ('Regular', 'Regular Center'), 
            ('Regular', 'Regular Center'), 
            ('Regular', 'Regular'), 
            ('Regular', 'Regular Center'), 
        )
        table_style = (
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            #('SPAN', (0,11), (0,12)),
        )
        self.add(template, [4, 6], self.get_style(para_style, template),
            table_style, styleTable=True, data=data
        )

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
            image = FileStorage.objects.get(pk=img_id)
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
        self.put('Приложение 4', 'Regular Right Italic', 0.5)
        self.zakl_header('визуального и измерительного контроля')
        self.measurers('визуальн')
        
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
            styleTable=True, spacer=.5
        )
        self.category_controller('ВИК')

    def appendix5_6(self):
        engine = Engine.objects.get(name=self.data['engine']['type'])
        zones_data = engine.control_zones()

        self.appendix5(zones_data)
        self.appendix6(zones_data)

    def appendix5(self, zones_data):
        self.new_page()
        self.put('Приложение 5', 'Regular Right Italic', 0.5)
        self.zakl_header('ультразвукового контроля')
        self.measurers('ультразвук')

        res = 'Техническое состояние элементов'
        self.put(res, 'Regular Bold Center', 0.2)

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
        self.category_controller('УК')

    def appendix6(self, zones_data):
        self.new_page()
        self.put('Приложение 6', 'Regular Right Italic', 0.5)
        self.put('Схема ультразвукового контроля', 'Regular Bold Center', 0.5)

        engine = Engine.objects.get(name=self.data['engine']['type'])
        self.put_photo(engine.meters, height=12.5)

        template = [
            ['1 &ndash; {control_zone_1}'],
            ['2 &ndash; {control_zone_2}'],
            ['3 &ndash; {control_zone_3}'],
            ['4 &ndash; {control_zone_4}'],
        ]
        para_style = (('Regular',), )
        table_style = (
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 0)
        )
        self.add(template, [8,2], self.get_style(para_style, template), table_style,
            data=zones_data, spacer=.5, hAlign='RIGHT'
        )

    def appendix7(self):
        self.new_page()
        self.put('Приложение 7', 'Regular Right Italic', 0.5)
        self.zakl_header('теплового контроля')
        self.measurers('инфракрас')
        self.spacer(.3)

        image1 = self.fetch_image(
            FileStorage.objects.get(pk=self.data['files']['therm1'][0]),
            height=7, width=7
        )
        image2 = self.fetch_image(
            FileStorage.objects.get(pk=self.data['files']['therm2'][0]),
            height=7, width=7
        )
        table_data = [[image1, image2]]
        table = Table(table_data,colWidths=self.columnize(5, 5))
        table.hAlign = 'CENTER'
        table_style = (
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        )
        table.setStyle(TableStyle(table_style))
        self.Story.append(table)
        self.spacer(0.2)

        therm_data = self.data['therm']
        tc = ThermClass.objects.get(pk=therm_data['tclass'])
        therm_data.update(dict(tclass=tc.get_name_display(), tclass_t_max=str(tc.t_max)))

        template = [
            ['Температурный класс', '{tclass}'],
            ['Максимально допустимая температура поверхности оболочки, °C', '{tclass_t_max}'],
            ['Расстояние до объекта, м', '{distance}'],
            ['Температура окружающей среды, °С', '{temp_env}'],
            ['Максимальная температура, °С', '{temp_max}'],
            ['Минимальная температура, °С', '{temp_min}'],
            ['Средняя температура, °С', '{temp_avg}'],
            ['Соответствие норме', '{correct}'],
        ]
        para_style = (
            ('Regular', 'Regular Center'),
        )
        self.add(template, [8,2], self.get_style(para_style, template), table_style,
            data=therm_data, styleTable=True, spacer=.5
        )
        self.category_controller('ТК')

    def appendix8(self):
        self.new_page()
        self.put('Приложение 8', 'Regular Right Italic', 0.5)
        self.zakl_header('вибродиагностического контроля')
        self.measurers('вибр')
        self.spacer(.3)

        template = [
            ['Зона контроля', 'Вертикальная', 'Горизонтальная', 'Осевая'],
            ['Подшипниковый узел со стороны привода', '{vert}', '{horiz}', '{axis}'],
            ['Подшипниковый узел с противоположной приводу стороны', '{reverse_vert}', '{reverse_horiz}', '{reverse_axis}'],
            ['Норма', '{norm}', '', ''],
        ]
        para_style = [
            ['Regular Bold Center', ],
            *[['Regular'] + ['Regular Center'] * 3]
        ]
        table_style = (
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('SPAN', (1,3), (3,3))
        )
        self.add(template, [4, 2, 2, 2], self.get_style(para_style, template), table_style,
            data=self.data['vibro'], styleTable=True, spacer=.5
        )
        text = '''
Вибродиагностический контроль электродвигателя проводился в соответствии с требованиями ГОСТ Р ИСО 10816-3-99 "Вибрация. Контроль состояния машин по результатам измерения вибрации на невращающихся частях. Часть 3. Промышленные машины номинальной мощностью более 15 кВт и номинальной скоростью от 120 до 15000 мин -1".
        '''
        self.put(text, 'Paragraph Justified Indent')
        self.put('Замеры проводились на подшипниковых узлах в трёх направлениях.',
            'Paragraph Justified Indent', .5)
        self.category_controller('ВД')

    def appendix9(self):
        self.new_page()
        self.put('Приложение 9', 'Regular Right Italic', 0.5)
        self.zakl_header('электрических измерений')

        self.spacer(.5)
        self.put('а) Измерения сопротивления обмотки статора постоянному току:', 'Regular Bold')
        self.measurers('микроомметр')
        self.put('Сопротивление обмотки статора, Ом', 'Regular Center', .2)

        template = [
            ['А-В', 'B-C', 'C-A'],
            ['{wireAB}', '{wireBC}', '{wireCA}'],
        ]
        para_style = [
            ['Regular Bold Center'],
            ['Regular Center']
        ]
        table_style = (
            ('BOTTOMPADDING', (0,0), (-1,0), 6),
            ('TOPPADDING', (0,0), (-1,0), 2),
        )
        self.add(template, [3, 4, 3], self.get_style(para_style, template), table_style,
            data=self.data['resistance'], styleTable=True, spacer=.5
        )
        self.spacer(.3)

        self.put('б)  Измерения сопротивления изоляции обмотки статора:', 'Regular Bold')
        self.measurers('сопротивления изоляции')
        self.put('Сопротивление изоляции, МОм', 'Regular Center', .2)
        template = [
            ['Фаза', 'А-0', 'B-0', 'C-0', 'А-В', 'B-C', 'C-A'],
            ['Сопротивление изоляции, Мом', '{isolation}', '{isolation}', '{isolation}', '&ndash;', '&ndash;', '&ndash;'],
        ]
        table_style = table_style + (
            ('BOTTOMPADDING', (0,1), (-1,1), 10),
            ('TOPPADDING', (0,1), (-1,1), 8),
        )
        self.add(template, [4, 1, 1, 1, 1, 1, 1], self.get_style(para_style, template), table_style,
            data=self.data['resistance'], styleTable=True, spacer=.3
        )
        self.put('Контроль электрических параметров в электродвигателе проводился в соответствии с требованиями ПТЭЭП, РД 34.45-51.300-97 Объём и нормы испытаний электрооборудования.', 'Paragraph Justified Indent', .3)
        self.category_controller('ЭЛ')

    def appendix10(self):
        self.new_page()
        self.put('Приложение 10', 'Regular Right Italic', 0.5)

        self.spacer(.5)
        template = [
            ['Перечень приборов'],
            [
                '№<br/>п/п', 'Тип прибора', 'Заводской номер<br/>прибора',
                'Свидетельство о<br/>поверке', 'Дата следующей<br/>поверки' 
            ]
        ]
        all_measurers = Measurer.objects.filter(id__in=self.data.get('measurers'))
        for num, measurer in enumerate(all_measurers, start=1):
            template.append([str(num), *measurer.details()])
        table_style = (
            ('SPAN', (0,0), (-1,0)),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ('TOPPADDING', (0,0), (-1,0), 7),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
        )
        para_style = (
            ('Regular Bold Center', ),
            ('Regular Center', ),
        )
        self.add(template, [1, 3, 2, 2, 2], self.get_style(para_style, template), table_style,
            styleTable=True, spacer=.5
        )

    def appendix11(self):
        self.new_page()

        self.put('Приложение 11', 'Regular Right Italic', 0.5)

        for img_id in self.data['files']['licenses']:
            image = FileStorage.objects.get(pk=img_id)
            self.put_photo(image)
            self.spacer(0.5)


    def category_controller(self, category):
        template = [
            ['Заключение: Соответствует. Двигатель годен к дальнейшей эксплуатации без ограничений.'],
            ['Контроль провел', '{fio}'],
            ['Удостоверение № {serial_number}, '
             'выдано {received} г., '
             'действительно по {expired} г.']
        ]
        para_style = (
            ('Zakluchenie', ),
            ('Regular Bold', 'Regular Right Bold'),
            ('Regular Center Italic', ),
        )
        table_style = (
            ('SPAN', (0,0), (-1,0)),
            ('SPAN', (0,-1), (-1,-1)),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ('TOPPADDING', (0,-1), (-1,-1), 10),
            ('ALIGN', (-1,1), (-1,1), 'RIGHT')
        )

        person = self.data.get('team')[category]
        emp = Employee.objects.get_by_full_name(person)
        if category == 'ЭЛ':
            cert = emp.ebcertificate
        else:
            cert = emp.get_certs_by_abbr(category)[0]
        self.add(template, [5,5], self.get_style(para_style, template), table_style,
            data=cert.info()
        )

    def zakl_header(self, control_type):
        table_style = (
            ('TOPPADDING', (-1,3), (-1,3), 15),
            ('TOPPADDING', (0,5), (-1,5), 15),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,4), (-1,4), 15),
            ('TOPPADDING', (0,-2), (-1,-1), 0),
        )
        para_style = [
            *[['Regular Bold Center', ]] * 5, ['Regular', ],
        ]
        data = self.data
        data.update({'control_type': control_type})
        template = self.static_data_plain('report_appendix_protocol_title.txt')
        self.add(template, [10], self.get_style(para_style, template), table_style,
            data=data
        )

    '''
        Prints table of selected measurers filtered by their purpose name
    
    '''
    def measurers(self, approx_category):
        self.put('<u>Средства контроля</u>:', 'Regular', .15)
        template = [
            [
                '№<br/>п/п', 'Тип прибора', 'Заводской номер<br/>прибора',
                'Свидетельство о<br/>поверке', 'Дата следующей<br/>поверки' 
            ]
        ]
        all_measurers = Measurer.objects.filter(
            id__in=self.data.get('measurers')
        ).filter(
            name__icontains=approx_category
        )
        for num, measurer in enumerate(all_measurers, start=1):
            template.append([str(num), *measurer.details()])
        table_style = (
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        )
        para_style = (('Regular Center', ),)
        self.add(template, [1, 3, 2, 2, 2], self.get_style(para_style, template), table_style,
            styleTable=True, spacer=.5
        )

        # Headers
        res = '<u>{}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{}:</u>'.format(
            ' '.join('Результаты').upper(),
            ' '.join('контроля').upper(),
        )
        self.put(res, 'Regular Bold Center', 0.3)

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

