import csv
from functools import partial
from datetime import datetime
from hashlib import sha1

from django.conf import settings
from django.utils import dateformat

from PIL import Image as PILImage
import environ

from reportlab.platypus.flowables import Flowable
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.platypus.doctemplate import BaseDocTemplate
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase import ttfonts

#import locale
#locale.setlocale(locale.LC_ALL, "")
#loc = partial(locale.format, "%.2f")


class MyDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kw):
        self.allowSplitting = 0
        self.appendix_colontitle = '32167'
        super(MyDocTemplate, self).__init__(filename, **kw)

    # Entries to the table of contents can be done either manually by
    # calling the addEntry method on the TableOfContents object or automatically
    # by sending a 'TOCEntry' notification in the afterFlowable method of
    # the DocTemplate you are using. The data to be passed to notify is a list
    # of three or four items countaining a level number, the entry text, the page
    # number and an optional destination key which the entry should point to.
    # This list will usually be created in a document template's method like
    # afterFlowable(), making notification calls using the notify() method
    # with appropriate data.
    def beforeDocument(self):
        self.appendixLetter = 'А'


    def afterFlowable(self, flowable):
        "Registers TOC entries."
        if flowable.__class__.__name__ == 'Paragraph':
            text = flowable.getPlainText()
            style = flowable.style.name
            #if style == 'Heading 1':
            #    level = 0
            if style == 'TOC Appendix' or style == 'TOC Appendix Hidden':
                level = 1
                text = 'Приложение {} {}'.format(self.appendixLetter, text.capitalize())
                self.appendixLetter = chr(ord(self.appendixLetter) + 1)
            elif style == 'TOC':
                level = 1
            else:
                return
            E = [level, text, self.page]
            #if we have a bookmark name append that to our notify data
            bn = getattr(flowable,'_bookmarkName',None)
            if bn is not None: E.append(bn)
            self.notify('TOCEntry', tuple(E))

#class Appendix_title(Flowable):
#    def __init__(self, width, text=''):
#        Flowable.__init__(self)
# 
#    def __repr__(self):
#        return "Appendix title(w=%s)" % self.width
# 
#    def draw(self):
#        self.canv.line(0, self.height, self.width, self.height)
#        self.canv.line(0, self.height + 2, self.width, self.height + 2)

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

class ReportMixin():
    def __init__(self, data, report, title):
        self.data = data
        self.report = report
        self.Story = []
        self.setup_fonts()
        self.styles = getSampleStyleSheet()
        self.setup_styles()

        self.doc = MyDocTemplate(self.report, pagesize=A4,
                                rightMargin=12,leftMargin=12,
                                topMargin=12,bottomMargin=12,
                                title=title,
                                #showBoundary=1
        )
        self.toc = TableOfContents()
        self.toc.levelStyles = [
            self.styles['TOCHeading1'],
            self.styles['TOCHeading2'],
        ]

        self.full_width = self.doc.width
        self.full_height = self.doc.height
        self.create()
        self.doc.multiBuild(self.Story)

    def add_to_toc(self, text, sty):
        data = str(text + sty.name).encode()
        bn = sha1(data).hexdigest()
        h = Paragraph(text + '<a name="%s"/>' % bn, sty)
        # store the bookmark name on the flowable so afterFlowable can see this
        h._bookmarkName = bn
        self.Story.append(h)

    def create(self):
        raise NotImplementedError('Define method "create"')

    '''
        Helper functions
    '''
    # Helper function for styling similar paragraphs
    def get_style(self, styles, template):
        rows_count = len(template)
        styles_count = len(styles)
        result = list(styles)
        result[-1:] = result[-1:] * (rows_count - (styles_count - 1))
        return result

    def get_csv(self, fname):
        contents = []
        with open(self.pathname(fname)) as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            for row in reader:
                contents.append(row)
        return contents

    def new_page(self):
        self.Story.append(PageBreak())

    def spacer(self, height):
        self.Story.append(Spacer(1, height * cm))

    def add(self, template, width, para_style, table_style, data={},
            spacer=None, hAlign='CENTER', styleTable=False):
        filled_template = self.values(template, data)
        table = self.table(filled_template, para_style, width, styleTable=styleTable)
        table.setStyle(TableStyle(table_style))
        table.hAlign = hAlign
        self.Story.append(table)
        if spacer:
            self.Story.append(Spacer(1, spacer * cm))

    @staticmethod
    def static_data_list(fname):
        file_ = str(settings.APPS_DIR.path('static', 'src', 'assets', fname))
        res = []
        with open(file_) as f:
            for n, line in enumerate(f, start=1):
                res.append([str(n), line])
        return res

    @staticmethod
    def static_data_plain(fname):
        file_ = str(settings.APPS_DIR.path('static', 'src', 'assets', fname))
        res = []
        with open(file_) as f:
            for line in f:
                res.append([line])
        return res

    @staticmethod
    def pathname(fname):
        return str(settings.APPS_DIR.path('static', 'src', 'assets', fname))

    @staticmethod
    def values(template, data):
        return list(map(lambda row: list(map(lambda cell: cell.format(**data), row)), template))

    @staticmethod
    def format_JS_dates(d, keys, format_='%d.%m.%Y'):
        for key in keys:
            dt = datetime.strptime(d[key].split('T')[0], '%Y-%m-%d')
            d[key] = dt.strftime(format_)

    @staticmethod
    def format_locale_JS_dates(d, keys, format_='d E Y'):
        for key in keys:
            dt = datetime.strptime(d[key].split('T')[0], '%Y-%m-%d')
            d[key] = dateformat.format(dt, format_) + ' г.'
            #d[key] = dt.strftime(format_)

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
        Functions for working with images
    '''
    def put_photo(self, filename, width=0, height=0):
        if hasattr(filename, 'name'):
            image = self.fetch_image(filename, width, height)
        else:
            image = self.fetch_static_image(filename, width, height)
        image.hAlign = 'CENTER'
        self.Story.append(image)

    def fetch_image(self, image, width=0, height=0):
        MEDIA_ROOT = environ.Path(settings.MEDIA_ROOT)
        file_ = str(MEDIA_ROOT.path(str(image.name)))
        return self.proc_image(file_, width, height)

    def fetch_static_image(self, img, width=0, height=0):
        file_ = str(settings.APPS_DIR.path('static', 'src', 'assets', 'images', img))
        return self.proc_image(file_, width, height)

    def proc_image(self, file_, width=0, height=0):
        image = PILImage.open(file_)
        maxsize = (
            (width * cm or self.full_width), 
            (height * cm or self.full_height)
        )
        # Get new image dimensions to fit in desired size
        image.thumbnail(maxsize, PILImage.ANTIALIAS)
        #print(file_, 'maxsize', maxsize, 'computed', image.width, image.height)
        return Image(file_, width=image.width, height=image.height)

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
            name='Regular Bold',
            fontName='Times Bold',
            fontSize=13,
            leading=16,
            alignment=TA_LEFT))
        self.styles.add(ParagraphStyle(
            name='Zakluchenie',
            fontName='Times Bold',
            firstLineIndent=0.7 * cm,
            fontSize=13,
            leading=16,
            alignment=TA_JUSTIFY))
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
            leading=13,
            #borderWidth=0.5,
            #borderColor=colors.black,
            alignment=TA_CENTER))
        self.styles.add(ParagraphStyle(
            name='Regular Center Small',
            fontName='Times',
            fontSize=11,
            leading=11,
            alignment=TA_CENTER))
        self.styles.add(ParagraphStyle(
            name='Regular Center Leading',
            fontName='Times',
            fontSize=13,
            leading=30,
            alignment=TA_CENTER))
        self.styles.add(ParagraphStyle(
            name='Regular Right',
            fontName='Times',
            fontSize=13,
            leading=16,
            alignment=TA_RIGHT))
        self.styles.add(ParagraphStyle(
            name='Regular Right Italic',
            fontName='Times Italic',
            fontSize=13,
            leading=16,
            alignment=TA_RIGHT))
        self.styles.add(ParagraphStyle(
            name='Regular Center Italic',
            fontName='Times Italic',
            fontSize=13,
            leading=16,
            alignment=TA_CENTER))
        self.styles.add(ParagraphStyle(
            name='Regular Center Italic Small',
            fontName='Times Italic',
            fontSize=11,
            leading=13,
            alignment=TA_CENTER))
        self.styles.add(ParagraphStyle(
            name='Regular Justified',
            fontName='Times',
            fontSize=13,
            leading=16,
            alignment=TA_JUSTIFY))
        self.styles.add(ParagraphStyle(
            name='Regular Justified Bold',
            fontName='Times Bold',
            fontSize=13,
            leading=16,
            alignment=TA_JUSTIFY))
        self.styles.add(ParagraphStyle(
            name='Regular Right Bold',
            fontName='Times Bold',
            fontSize=13,
            leading=16,
            alignment=TA_RIGHT))
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
        self.styles.add(ParagraphStyle(
            name='TOC Regular',
            fontName='Times',
            fontSize=13,
            leading=13,
            leftIndent=88,
            firstLineIndent=-88,
            alignment=TA_LEFT))
        # Container's Report specific styles. Until they lies here
        self.styles.add(ParagraphStyle(
            name='Text',
            fontName='Times',
            fontSize=14,
            leading=21,
            bulletIndent=18,
            firstLineIndent=1.25 * cm,
            alignment=TA_JUSTIFY))
        self.styles.add(ParagraphStyle(
            name='Text Simple',
            fontName='Times',
            fontSize=14,
            leading=18,
            bulletIndent=18,
            alignment=TA_LEFT))
        self.styles.add(ParagraphStyle(
            name='Text Simple Indent',
            fontName='Times',
            fontSize=14,
            leading=22,
            leftIndent=24,
            bulletIndent=3,
            alignment=TA_JUSTIFY))
        self.styles.add(ParagraphStyle(
            name='Text Simple Bold',
            fontName='Times Bold',
            fontSize=14,
            leading=18,
            bulletIndent=18,
            alignment=TA_LEFT))
        self.styles.add(ParagraphStyle(
            name='Text Simple Right',
            fontName='Times',
            fontSize=14,
            leading=18,
            bulletIndent=18,
            alignment=TA_RIGHT))
        self.styles.add(ParagraphStyle(
            name='Text Simple Center',
            fontName='Times',
            fontSize=14,
            leading=18,
            bulletIndent=18,
            alignment=TA_CENTER))
        self.styles.add(ParagraphStyle(
            name='Text Simple Center Bold',
            fontName='Times Bold',
            fontSize=14,
            leading=18,
            bulletIndent=18,
            alignment=TA_CENTER))
        self.styles.add(ParagraphStyle(
            name='Text Simple Dense',
            fontName='Times',
            fontSize=14,
            leading=14,
            bulletIndent=18,
            alignment=TA_LEFT))
        self.styles.add(ParagraphStyle(
            name='Text Simple Height',
            fontName='Times',
            fontSize=14,
            leading=21,
            #firstLineIndent=-0.40 * cm,
            #bulletIndent=0 * cm,
            #leftIndent=0.40 * cm,
            alignment=TA_JUSTIFY))
        self.styles.add(ParagraphStyle(
            name='Text Simple Center Dense',
            fontName='Times',
            fontSize=14,
            leading=14,
            bulletIndent=18,
            alignment=TA_CENTER))
        self.styles.add(ParagraphStyle(
            name='TOC',
            fontName='Times Bold',
            fontSize=14,
            leading=21,
            firstLineIndent=1.25 * cm,
            alignment=TA_LEFT))
        self.styles.add(ParagraphStyle(
            name='TOC Appendix',
            fontName='Times Bold',
            fontSize=14,
            leading=18,
            alignment=TA_CENTER))
        self.styles.add(ParagraphStyle(
            name='TOC Appendix Hidden',
            fontName='Times Bold',
            fontSize=0,
            textColor=colors.white,
            alignment=TA_CENTER))
        self.styles.add(ParagraphStyle(
            name='TOCHeading1',
            fontName='Times Bold',
            fontSize=14,
            leading=21,
            alignment=TA_CENTER))
        self.styles.add(ParagraphStyle(
            name='TOCHeading2',
            fontName='Times',
            fontSize=14,
            leading=21,
            firstLineIndent=-3.25 * cm,
            leftIndent=3.25 * cm,
            alignment=TA_LEFT))
