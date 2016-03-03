from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase import ttfonts

def make_report(report):
    doc = SimpleDocTemplate(report, pagesize=A4,
                            rightMargin=12,leftMargin=12,
                            topMargin=12,bottomMargin=12,
                            title='Новый отчет',
                            #showBoundary=1,
    )

    Story=[]
     
    font_setting()

    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_CENTER))
    styles.add(ParagraphStyle(
        name='Heading 1 Bold',
        fontName='Times Bold',
        fontSize=14,
        leading=20,
        alignment=TA_CENTER))
    styles.add(ParagraphStyle(
        name='Heading 1',
        fontName='Times',
        #borderWidth=0.3,
        #borderColor=colors.black,
        fontSize=13,
        leading=18,
        alignment=TA_CENTER))
    styles.add(ParagraphStyle(
        name='Signature',
        fontName='Times',
        #borderWidth=0.3,
        #borderColor=colors.black,
        fontSize=13,
        leading=30,
        alignment=TA_CENTER))

    ptext = 'ПАО "ГАЗПРОМ"<br/>РОССИЙСКАЯ ФЕДЕРАЦИЯ<br/>ООО «ГАЗМАШПРОЕКТ»'
    Story.append(Paragraph(ptext, styles["Heading 1 Bold"]))
    Story.append(Spacer(1, 0.5*cm))

    ptext = '''<b>"Согласовано"</b><br/><br/>
    Заместитель генерального директора по производству - Главный инженер 
    Шеморданского ЛПУ МГ<br/>
    ООО"Газпром трансгаз Ставрополь"
    '''
    left_column = Paragraph(ptext, styles["Heading 1"]) 
    ptext = '''<b>"Утверждаю"</b><br/><br/>
    Директор филиала<br/>
    ООО «ГАЗМАШПРОЕКТ»<br/>
    «НАГАТИНСКИЙ»
    '''
    right_column = Paragraph(ptext, styles["Heading 1"]) 
    table_data = [[left_column, right_column]]
    
    ptext = '''_____________________Ю.В. Иванов
    "_____"_____________________201   г.
    '''
    left_column = Paragraph(ptext, styles["Signature"]) 
    ptext = '''________________А.Н. Бондаренко
    "_____"___________________201   г.
    '''
    right_column = Paragraph(ptext, styles["Signature"]) 
    table_data.extend([[left_column, right_column]])
    table = Table(table_data)
    table.setStyle(TableStyle([
        #('INNERGRID', (0,0), (-1,-1), 0.1, colors.black),
        #('BOX', (0,0), (-1,-1), 1.0, colors.black),

        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('RIGHTPADDING', (0,0), (0,-1), 1.5*cm),
        ('LEFTPADDING', (-1,0), (-1,-1), 1.5*cm),
    ]))
    Story.append(table)
     
    ## Create return address
    #ptext = '<font size=12>%s</font>' % full_name
    #Story.append(Paragraph(ptext, styles["Normal"]))       
    #for part in address_parts:
    #    ptext = '<font size=12>%s</font>' % part.strip()
    #    Story.append(Paragraph(ptext, styles["Normal"]))   
    # 
    #Story.append(Spacer(1, 12))
    #ptext = '<font size=12>Dear %s:</font>' % full_name.split()[0].strip()
    #Story.append(Paragraph(ptext, styles["Normal"]))
    #Story.append(Spacer(1, 12))
    # 
    #ptext = '<font size=12>We would like to\
    #        welcome you to our subscriber base for %s Magazine! \
    #        You will receive %s issues at the excellent introductory price of $%s. Please respond by\
    #        %s to start receiving your subscription and get the following free gift: %s.</font>' % (magName, 
    #                                                                                                issueNum,
    #                                                                                                subPrice,
    #                                                                                                limitedDate,
    #                                                                                                freeGift)
    #Story.append(Paragraph(ptext, styles["Justify"]))
    #Story.append(Spacer(1, 12))
    # 
    # 
    #ptext = '<font size=12>Thank you very much and we look forward to serving you.</font>'
    #Story.append(Paragraph(ptext, styles["Justify"]))
    #Story.append(Spacer(1, 12))
    #ptext = '<font size=12>Sincerely,</font>'
    #Story.append(Paragraph(ptext, styles["Normal"]))
    #Story.append(Spacer(1, 48))
    #ptext = '<font size=12>Ima Sucker</font>'
    #Story.append(Paragraph(ptext, styles["Normal"]))
    #Story.append(Spacer(1, 12))
    doc.build(Story)

def font_setting():
    fonts = (
        ('Times', 'times.ttf'), 
        ('Times Bold', 'timesbd.ttf'),
        ('Times Italic', 'timesi.ttf'),
        ('Times Bold Italic', 'timesbi.ttf'),
    )
    list(map(register_fonts, *zip(*fonts)))
    pdfmetrics.registerFontFamily(
        'Times', normal='Times', bold='Times Bold',
        italic='Times Bold Italic', boldItalic='Times Bold Italic')

def register_fonts(font_name, font_file):
    #print('Registering font {} from file {}'.format(font_name, font_file))
    MyFontObject = ttfonts.TTFont(font_name, font_file)
    pdfmetrics.registerFont(MyFontObject)
 
