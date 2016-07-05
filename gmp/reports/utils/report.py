from datetime import datetime
from functools import partial
from itertools import chain
from json import dumps

from django.forms.models import model_to_dict

from reportlab.platypus import Paragraph, Image, NextPageTemplate, TableStyle, KeepTogether, Preformatted, Table, Spacer
from reportlab.platypus.frames import Frame
from reportlab.platypus.doctemplate import PageTemplate
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle as PS
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT

from gmp.authentication.models import Employee
from gmp.certificate.models import Certificate
from gmp.inspections.models import Organization, LPU
from gmp.departments.models import Measurer
from gmp.engines.models import Engine, ThermClass, Connection
from gmp.filestorage.models import FileStorage

from .helpers import ReportMixin


class Report(ReportMixin):
    def __init__(self, data, report, title):
        toc_styles = ('TOCHeading4', 'TOCHeading4')
        super().__init__(data, report, title, leftMargin=1.2, rightMargin=.5, toc_styles=toc_styles)

    def create(self):
        self.proc_excel_data()
        self.setup_page_templates(self.doc, self.header_content())

        if not self.data['files'].get('excel'):
            self.format_JS_dates(self.data['engine'], ('manufactured_at', 'started_at'), '%Y')
            self.format_JS_dates(self.data['engine'], ('new_date',))
            self.format_JS_dates(self.data, ('workBegin', 'workEnd'))
            self.format_JS_dates(self.data['order'], ('date',))

        self.Story.append(NextPageTemplate('Title'))
        self.toc_entry = [
            {
                'width': 0.2,
                'font':  {
                    'name': 'Regular Bold',
                    'fontName': 'Times Bold',
                    'fontSize': 13,
                    'leading': 14,
                    'alignment': TA_CENTER
                }
            },
            {
                'width': 0.8,
                'font':  {
                    'name': 'Regular',
                    'fontName': 'Times Bold',
                    'fontSize': 13,
                    'leading': 14,
                    'alignment': TA_LEFT
                }
            }

        ]
        self.page1()
        self.Story.append(NextPageTemplate('Content'))
        self.put_toc()
        self.page3()
        self.toc_entry = [
            {
                'width': 0.2,
                'font':  {
                    'name': 'Regular Bold',
                    'fontName': 'Times Bold',
                    'fontSize': 13,
                    'leading': 14,
                    'alignment': TA_CENTER
                }
            },
            {
                'width': 0.8,
                'font':  {
                    'name': 'Regular',
                    'fontName': 'Times',
                    'fontSize': 13,
                    'leading': 14,
                    'alignment': TA_LEFT
                }
            }

        ]
        self.appendix1()
        self.appendix2()
        self.appendix3()
        self.appendix4()
        self.appendix5_6()
        self.appendix7()
        self.appendix8()
        self.appendix9()
        self.appendix10()
        self.appendix11()

    def proc_excel_data(self):
        rows_w_values = self.read_excel_data()
        self.data['obj_data']['ks'] = rows_w_values['Наименование КС или установки']
        self.data['obj_data']['plant'] = rows_w_values['Название цеха']
        self.data['obj_data']['location'] = rows_w_values['Место установки']
        self.data['obj_data']['detail_info'] = rows_w_values['Краткая характеристика и назначение объекта экспертизы']

        self.data['docs'] = rows_w_values['Документация, предоставленная заказчиком']

        self.data['engine']['serial_number'] = rows_w_values['Заводской номер']
        self.data['engine']['station_number'] = rows_w_values['Станционный номер']
        self.data['engine']['manufactured_at'] = rows_w_values['Год изготовления']
        self.data['engine']['started_at'] = rows_w_values['Год ввода в эксплуатацию']
        self.data['engine']['new_date'] = rows_w_values['Дата продления срока эксплуатации']

        self.data['workBegin'] = rows_w_values['Дата начала работ']
        self.data['workEnd'] = rows_w_values['Дата окончания работ']

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


    def put_toc(self):
        self.new_page()
        self.put('Содержание', 'Regular Bold Center', 0.5)
        self.Story.append(self.toc)

    def page1(self):
        self.put_photo('zakl_header_img.jpg')
        self.spacer(6)

        template = [
            ['ЗАКЛЮЧЕНИЕ № 1-2/1715-10-14'],
            ['''ЭКСПЕРТИЗЫ ПРОМЫШЛЕННОЙ БЕЗОПАСНОСТИ НА ТЕХНИЧЕСКОЕ УСТРОЙСТВО,
                ЭКСПЛУАТИРУЕМОЕ НА ОПАСНОМ ПРОИЗВОДСТВЕННОМ ОБЪЕКТЕ'''],
            ['<strong>Объект:</strong> Взрывозащищённый электродвигатель {engine[type]}'],
            ['станционный № {engine[station_number]} зав.№ {engine[serial_number]}'],
            ['<strong>Владелец:</strong> {obj_data[org][name]}'],
            ['''<strong>Место установки:</strong> {obj_data[lpu][name]}, {obj_data[ks]},
                {obj_data[plant]}, {obj_data[location]}'''],
            ['№_____________________________________']
        ]
        rows = len(template)
        para_style = [
            *[['Heading 1 Bold']] * 2,
            *[['Regular Center Tall']] * (rows - 2),
        ]
        table_style = (('BOTTOMPADDING', (0,0), (-1,-1), 10), )
        self.add(template, [8], para_style, table_style,
            data=self.data, hAlign='CENTER')

    def add_to_toc(self, *entries):
        toc_entry = []
        for num, item in enumerate(self.toc_entry):
            toc_entry.append({ **item, 'text': entries[num]})
        json_toc_entry = dumps(toc_entry)
        super().add_to_toc(json_toc_entry, self.styles['TOC Hidden'])

    def page3(self):
        self.new_page()
        self.add_to_toc('1', 'Вводная часть')
        table_style = (
            ('BOTTOMPADDING', (0,1), (-1,1), 10),
            ('BOTTOMPADDING', (0,0), (-1,0), 10),
            ('BOTTOMPADDING', (0,2), (-1,-2), 0),
            ('BOTTOMPADDING', (0,-1), (-1,-1), 10),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        )
        para_style_full = (
            ('Regular Center Tall', 'Regular Center Tall'),
            ('Regular Center Tall', 'Regular Justified'),
        )
        para_style = (('Regular Center Tall', 'Regular Justified'), )
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
        self.add_to_toc('2', 'Объект экспертизы')
        template = self.get_csv('report_main_content2.csv')
        self.add(template, [1, 9], self.get_style(para_style_full, template), table_style[1:],
            data=self.data, spacer=0.5)

        ## 3
        self.add_to_toc('3', 'Данные о заказчике')
        template = self.get_csv('report_main_content3.csv')
        org_name = self.data['obj_data']['org']['name']
        org = Organization.objects.get(name=org_name)
        self.add(template, [1, 9], self.get_style(para_style_full, template), table_style[1:],
            data=model_to_dict(org), spacer=0.5)

        ## 4
        self.add_to_toc('4', 'Цель экспертизы промышленной безопасности')
        template = self.get_csv('report_main_content4.csv')
        self.add(template, [1, 9], self.get_style(para_style_full, template), table_style[1:],
            data=self.data['engine'], spacer=0.5)

        ### 5
        self.add_to_toc('5', 'Сведения о рассмотренных документах')
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
        self.add_to_toc('6', 'Краткая характеристика и назначение объекта экспертизы')
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
        self.add_to_toc('7', 'Перечень работ, выполненных при проведении экспертизы промышленной безопасности')
        template = self.get_csv('report_main_content7.csv')
        self.add(template, [1, 9], self.get_style(para_style_full, template), table_style[1:],
            spacer=0.5)

        ## 8
        self.add_to_toc('8', 'Результаты экспертизы промышленной безопасности')
        template = self.get_csv('report_main_content8.csv')
        self.add(template, [1, 9], self.get_style(para_style_full, template), table_style[1:],
            data=self.data, spacer=0.5)

        ## 9
        self.add_to_toc('9', 'Выводы заключения экспертизы')
        template = self.get_csv('report_main_content9.csv')
        first_N_rows = template[:-1]
        text = self.get(first_N_rows, [1, 9], self.get_style(para_style_full, first_N_rows), table_style[1:],
            data=self.data)

        table_style = ()
        para_style = (('Regular', 'Regular Right'), )
        last_row = template[-1:]
        expert = self.get(last_row, [5, 5], self.get_style(para_style, last_row), table_style)

        self.Story.append(KeepTogether([text, Spacer(0, .5 * cm), expert]))

    def appendix1(self):
        self.new_page()
        self.add_to_toc('Приложение 1', 'Руководящая нормативно-техническая документация')
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
            ('Regular Center Tall', 'Regular Justified',),
        )
        para_style = (('Regular Center Tall', 'Regular Justified'), )
        template = self.static_data_plain('report_appendix1.txt')
        numbered_list = enumerate(chain.from_iterable(template[2:]), start=1)
        stringified_numbered_list = list(map(lambda x: [str(x[0]), x[1]], numbered_list))
        template = template[:2] + stringified_numbered_list
        self.add(template, [1,9], self.get_style(para_style_full, template), table_style)

    def appendix2(self):
        self.new_page()

        self.add_to_toc('Приложение 2', 'Программа проведения экспертизы промышленной безопасности по продлению срока безопасной эксплуатации взрывозащищённого электродвигателя')
        self.put('Приложение 2', 'Regular Right Italic', 0.5)

        for img in self.data['files']['main']:
            image = FileStorage.objects.get(pk=img['id'])
            self.put_photo(image.fileupload)
            self.spacer(0.5)

    def appendix3(self):
        self.new_page()
        self.add_to_toc('Приложение 3', 'Технические данные объекта')

        data = self.data.get('engine')
        engine = Engine.objects.get(name=data.get('type'))
        engine_data = engine.details()
        connection = Connection.objects.get(pk=data['connection'])
        data.update(engine_data, connection=str(connection))

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
        para_style = (('Regular', 'Regular Center Tall'), )
        table_style = (
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('TOPPADDING', (0,0), (-1,-1), 2),
        )
        self.add(template, [5, 5], self.get_style(para_style, template), table_style,
            data=data, styleTable=True
        )

    def appendix4(self):
        self.new_page()
        self.add_to_toc('Приложение 4', 'Протокол визуального и измерительного контроля')
        self.put('Приложение 4', 'Regular Right Italic', 0.5)
        self.zakl_header('визуального и измерительного контроля')
        self.measurers('визуальн')
        
        res = 'КОНТРОЛЬ ПАРАМЕТРОВ ВЗРЫВОЗАЩИТЫ'
        self.put(res, 'Regular Center Tall', 0.2)

        # Measure data
        table_data = [[
            self.fetch_static_image('engine_details_scheme_1.jpg', height=5),
            self.fetch_static_image('engine_details_scheme_2.jpg', height=5),
            self.fetch_static_image('engine_details_scheme_3.jpg', height=5),
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
            ('Regular Bold Center', ), ('Regular Center Tall', ),
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
        para_style = (('Regular', 'Regular Center Tall'),)
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
            ('Regular', 'Regular Center Tall'),
            ('Regular Bold', ),
            ('Regular', 'Regular Center Tall'),
        )
        table_style = table_style + (
            ('BOTTOMPADDING', (0,0), (0,0), 0),
            ('BOTTOMPADDING', (0,2), (0,2), 0),
            ('SPAN', (0,0), (-1,0)),
            ('SPAN', (0,2), (-1,2)),
        )
        self.add(template, [8, 2], self.get_style(para_style, template), table_style,
            styleTable=True, spacer=.3
        )
        self.category_controller('ВИК')

    def appendix5_6(self):
        engine = Engine.objects.get(name=self.data['engine']['type'])
        zones_data = engine.control_zones()

        self.appendix5(zones_data)
        self.appendix6(zones_data)

    def appendix5(self, zones_data):
        self.new_page()
        self.add_to_toc('Приложение 5', 'Протокол ультразвукового контроля')
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
            ['Regular', *['Regular Center Tall'] * 5],
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
        self.add_to_toc('Приложение 6', 'Схема ультразвукового контроля')
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
        self.add_to_toc('Приложение 7', 'Протокол теплового контроля')
        self.put('Приложение 7', 'Regular Right Italic', 0.5)
        self.zakl_header('теплового контроля')
        self.measurers('инфракрас')
        self.spacer(.3)

        image1 = self.fetch_image(
            FileStorage.objects.get(pk=self.data['files']['therm1'][0]['id']).fileupload,
            height=7, width=7
        )
        image2 = self.fetch_image(
            FileStorage.objects.get(pk=self.data['files']['therm2'][0]['id']).fileupload,
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
            ('Regular', 'Regular Center Tall'),
        )
        self.add(template, [8,2], self.get_style(para_style, template), table_style,
            data=therm_data, styleTable=True, spacer=.5
        )
        self.category_controller('ТК')

    def appendix8(self):
        self.new_page()
        self.add_to_toc('Приложение 8', 'Протокол вибродиагностического контроля')
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
            *[['Regular'] + ['Regular Center Tall'] * 3]
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
        self.add_to_toc('Приложение 9', 'Протокол  электрических измерений')
        self.put('Приложение 9', 'Regular Right Italic', 0.5)
        self.zakl_header('электрических измерений')

        self.spacer(.4)
        self.put('а) Измерения сопротивления обмотки статора постоянному току:', 'Regular Bold')
        self.measurers('микроомметр')
        self.put('Сопротивление обмотки статора, Ом', 'Regular Center Tall', .2)

        template = [
            ['А-В', 'B-C', 'C-A'],
            ['{wireAB}', '{wireBC}', '{wireCA}'],
        ]
        para_style = [
            ['Regular Bold Center'],
            ['Regular Center Tall']
        ]
        table_style = (
            ('BOTTOMPADDING', (0,0), (-1,0), 6),
            ('TOPPADDING', (0,0), (-1,0), 2),
        )
        self.add(template, [3, 4, 3], self.get_style(para_style, template), table_style,
            data=self.data['resistance'], styleTable=True, spacer=.3
        )

        self.put('б)  Измерения сопротивления изоляции обмотки статора:', 'Regular Bold')
        self.measurers('сопротивления изоляции')
        self.put('Сопротивление изоляции, МОм', 'Regular Center Tall', .2)
        template = [
            ['Фаза', 'А-0', 'B-0', 'C-0', 'А-В', 'B-C', 'C-A'],
            ['Сопротивление изоляции, Мом', '{isolation}', '{isolation}', '{isolation}', '&ndash;', '&ndash;', '&ndash;'],
        ]
        table_style = table_style + (
            ('BOTTOMPADDING', (0,1), (-1,1), 8),
            ('TOPPADDING', (0,1), (-1,1), 6),
        )
        self.add(template, [4, 1, 1, 1, 1, 1, 1], self.get_style(para_style, template), table_style,
            data=self.data['resistance'], styleTable=True, spacer=.3
        )
        self.put('Контроль электрических параметров в электродвигателе проводился в соответствии с требованиями ПТЭЭП, РД 34.45-51.300-97 Объём и нормы испытаний электрооборудования.', 'Paragraph Justified Indent', .3)
        self.category_controller('ЭЛ')

    def appendix10(self):
        self.new_page()
        self.add_to_toc('Приложение 10', 'Перечень приборов и инструментов')
        self.put('Приложение 10', 'Regular Right Italic', 0.5)

        self.spacer(.5)
        template = [
            ['Перечень приборов'],
            [
                '№<br/>п/п', 'Тип прибора', 'Заводской номер<br/>прибора',
                'Свидетельство о<br/>поверке', 'Дата следующей<br/>поверки' 
            ]
        ]
        all_measurers = Measurer.objects.filter(id__in=self.data.get('measurers').get('selected'))
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
            ('Regular Center Tall', ),
        )
        self.add(template, [1, 3, 2, 2, 2], self.get_style(para_style, template), table_style,
            styleTable=True, spacer=.5
        )

    def appendix11(self):
        self.new_page()

        self.add_to_toc('Приложение 11', 'Копии лицензий экспертной организации на право проведения экспертизы промышленной безопасности, копии свидетельств об аккредитации в системе экспертизы промышленной безопасности, копии удостоверений экспертов и специалистов по неразрушающему контролю')
        self.put('Приложение 11', 'Regular Right Italic', 0.5)

        for img in self.data['files']['licenses']:
            image = FileStorage.objects.get(pk=img['id'])
            self.put_photo(image.fileupload)
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
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('TOPPADDING', (0,-1), (-1,-1), 5),
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
            id__in=self.data.get('measurers').get('selected')
        ).filter(
            name__icontains=approx_category
        )
        for num, measurer in enumerate(all_measurers, start=1):
            template.append([str(num), *measurer.details()])
        table_style = (
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        )
        para_style = (('Regular Center Tall', ),)
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
    def setup_page_templates(self, doc, header_content):
        frame_with_header = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
                bottomPadding=0, leftPadding=0, rightPadding=0, topPadding=0,
                id='with_header')
        template_title = PageTemplate(id='Title', frames=frame_with_header, onPage=partial(self.header, content=header_content))

        frame_full = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='no_header')
        template_content = PageTemplate(id='Content', frames=frame_full, onPage=self.header)

        doc.addPageTemplates([template_title, template_content])

    @staticmethod
    def header(canvas, doc, content=None):
        canvas.saveState()

        if not content:
            style = PS(
                'Page Number',
                fontName='Times',
                fontSize=13)
            pageNumber = Paragraph(str(canvas.getPageNumber()), style=style)
            w, h = pageNumber.wrap(doc.width, doc.topMargin)
            pageNumber.drawOn(canvas, doc.width + doc.leftMargin - 10, h + 10)
        else: 
            w, h = content[0].wrap(doc.width, doc.topMargin)
            content[0].drawOn(canvas, (doc.width + w)/2 - doc.leftMargin, 120)

            w, h = content[1].wrap(doc.width, doc.topMargin)
            content[1].drawOn(canvas, doc.leftMargin + doc.width - w/2, h + 30)

        canvas.restoreState()

    def header_content(self):
        date_string = '"____"{:_>15}'.format('_') + '201&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;г'
        fio_string = '{fio:_>25}'
        template = [
            ['Директор филиала<br/>ООО «ГАЗМАШПРОЕКТ» «НАГАТИНСКИЙ»'],
            [fio_string.format(fio='Р.Ю. Ерин')],
            [date_string]   
        ]
        rows = len(template)
        styles = [
            *[['Regular Center Tall']] * rows,
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

