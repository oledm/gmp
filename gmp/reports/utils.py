from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase import ttfonts

from gmp.authentication.models import Employee

class Report():
    def __init__(self):
        self.Story = []
        self.styles = getSampleStyleSheet()

    def make_report(self, report, data):
        doc = SimpleDocTemplate(report, pagesize=A4,
                                rightMargin=12,leftMargin=12,
                                topMargin=12,bottomMargin=12,
                                title='Паспорт двигателя ' + data['engine']['type'],
                                #showBoundary=1,
        )
         
        self.setup_fonts()
        self.setup_styles()


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
        
        ptext = '''_____________________Ю.В. Иванов
        "_____"____________________201    г.
        '''
        left_column = Paragraph(ptext, self.styles["Signature"]) 
        ptext = '''________________А.Н. Бондаренко
        "_____"__________________201<pre>      </pre> г.
        '''
        right_column = Paragraph(ptext, self.styles["Signature"]) 
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
        self.Story.append(Spacer(1, 1 * cm))

        self.mput([
            'ПАСПОРТ 1-2/1715-10-14',
            'ТЕХНИЧЕСКОГО СОСТОЯНИЯ',
            'ВЗРЫВОЗАЩИЩЁННОГО ЭЛЕКТРОДВИГАТЕЛЯ',
        ], 'MainTitle', 1)

        engine = data.get('engine')
        self.mput([
            'ОБЪЕКТ:',
            'ТИП: {type} зав.№ {serial_number}'.format(**engine),
        ], 'MainTitle', 1)

        self.Story.append(PageBreak())
        self.put('Дата обследования: ХХ.ХХ.ХХХХ', 'Heading 1', 1)

        for person in data.get('team'):
            print('name {name}, rank {rank}'.format(**person))
            print(Employee.objects.full_name_is(person['name']))
            self.put(person['name'], 'Heading 1')
            
        doc.build(self.Story)


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
            name='MainTitle',
            fontName='Times Bold',
            #borderWidth=0.3,
            #borderColor=colors.black,
            fontSize=16,
            leading=20,
            alignment=TA_CENTER))
