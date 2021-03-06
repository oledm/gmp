import csv
from functools import partial, reduce
from datetime import datetime
from hashlib import sha1

from django.conf import settings
from django.utils import dateformat

from PIL import Image as PILImage
import environ

from reportlab.platypus.flowables import Flowable, KeepInFrame
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.platypus.doctemplate import BaseDocTemplate
from .tableofcontents import TableOfContents
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase import ttfonts

#import locale
#locale.setlocale(locale.LC_ALL, "")
#loc = partial(locale.format, "%.2f")

from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl

from .excel_import import ExcelImporter
from gmp.filestorage.models import FileStorage


class PdfImage(Flowable):

    def __init__(self, filename, width=None, height=None, kind='bound',
                                     mask=None, lazy=True, srcinfo=None):
        Flowable.__init__(self)
        self._kind = kind
        page = PdfReader(filename, decompress=False).pages[0]
        self.xobj = pagexobj(page)
        self.imageWidth, self.imageHeight = imageWidth, imageHeight = self.xobj.w, self.xobj.h
        width = width or imageWidth
        height = height or imageHeight
        if kind in ['bound','proportional']:
            factor = min(float(width)/imageWidth,float(height)/imageHeight)
            width = factor * imageWidth
            height = factor * imageHeight
        self.drawWidth = width
        self.drawHeight = height

    def wrap(self, aW, aH):
        return self.drawWidth, self.drawHeight

    def drawOn(self, canv, x, y, _sW=0, width=0, height=0):
        if _sW > 0 and hasattr(self, 'hAlign'):
            a = self.hAlign
            if a in ('CENTER', 'CENTRE', TA_CENTER):
                x += 0.5*_sW
            elif a in ('RIGHT', TA_RIGHT):
                x += _sW
            elif a not in ('LEFT', TA_LEFT):
                raise ValueError("Bad hAlign value " + str(a))

        xobj = self.xobj
        xobj_name = makerl(canv._doc, xobj)

        xscale = (width or self.drawWidth) / xobj.w
        yscale = (height or self.drawHeight) / xobj.h
        x -= xobj.x * xscale
        y -= xobj.y * yscale

        canv.saveState()
        canv.translate(x, y)
        canv.scale(xscale, yscale)
        canv.doForm(xobj_name)
        canv.restoreState()

    def _restrictSize(self,aW,aH):
        if self.drawWidth>aW+_FUZZ or self.drawHeight>aH+_FUZZ:
            self._oldDrawSize = self.drawWidth, self.drawHeight
            factor = min(float(aW)/self.drawWidth,float(aH)/self.drawHeight)
            self.drawWidth *= factor
            self.drawHeight *= factor
        return self.drawWidth, self.drawHeight

    def getSize(self):
        return self.drawWidth, self.drawHeight



class MyDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kw):
        self.allowSplitting = 0
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
            if style == 'TOC Appendix' or style == 'TOC Appendix Hidden':
                level = 1
                # Skip russain letter 'З' and 'Й'
                if self.appendixLetter ==  'З' or self.appendixLetter ==  'Й':
                    self.appendixLetter = chr(ord(self.appendixLetter) + 1)
                text = 'Приложение&nbsp;&nbsp;&nbsp;{}&nbsp;&nbsp;&nbsp;{}'.format(self.appendixLetter, text.capitalize())
                self.appendixLetter = chr(ord(self.appendixLetter) + 1)
            elif style == 'TOC' or style == 'TOC Hidden':
                level = 1
            elif style == 'TOC Hidden wo dots':
                level = 0
            else:
                return
            E = [level, text, self.page]
            #if we have a bookmark name append that to our notify data
            bn = getattr(flowable,'_bookmarkName',None)
            if bn is not None: E.append(bn)
            self.notify('TOCEntry', tuple(E))


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
    def __init__(self, data, report, title,
                 toc_styles=[],
                 leftMargin=3,
                 rightMargin=.7,
                 topMargin=1,
                 bottomMargin=1,
                 ):
        self.data = data
        self.report = report
        self.Story = []
        self.setup_fonts()
        self.styles = getSampleStyleSheet()
        self.setup_styles()

        self.doc = MyDocTemplate(self.report, pagesize=A4,
                                leftMargin=leftMargin * cm,
                                rightMargin=rightMargin * cm,
                                topMargin=topMargin * cm,
                                bottomMargin=bottomMargin * cm,
                                title=title
        )
        self.toc = TableOfContents()
        self.toc.levelStyles = list(map(lambda x: self.styles[x], toc_styles)) or [
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

    def add_to_toc_and_return(self, text, sty):
        data = str(text + sty.name).encode()
        bn = sha1(data).hexdigest()
        h = Paragraph(text + '<a name="%s"/>' % bn, sty)
        # store the bookmark name on the flowable so afterFlowable can see this
        h._bookmarkName = bn
        return h

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

    #def add(self, template, width, para_style, table_style, data={},
    #        spacer=None, hAlign='CENTER', styleTable=False):
    def add(self, template, width, para_style, table_style, **kwargs):
        table = self.get(template, width, para_style, table_style, **kwargs)
        self.Story.append(table)
        if kwargs.get('spacer'):
            self.Story.append(Spacer(1, kwargs.get('spacer') * cm))

    def get(self, template, width, para_style, table_style, data={},
            spacer=None, hAlign='CENTER', styleTable=False):
        filled_template = self.values(template, data)
        table = self.table(filled_template, para_style, width, styleTable=styleTable)
        table.setStyle(TableStyle(table_style))
        table.hAlign = hAlign
        return table

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
    def format_JS_dates(d, keys, format_='%d.%m.%Y', format_from='%Y-%m-%d'):
        for key in keys:
            dt = datetime.strptime(d[key].split('T')[0], format_from)
            d[key] = dt.strftime(format_)

    @staticmethod
    def format_locale_JS_dates(d, keys, format_='d E Y', format_from='%Y-%m-%d'):
        for key in keys:
            dt = datetime.strptime(d[key].split('T')[0], format_from)
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

    def put_one_page(self, objects):
        inframe = KeepInFrame(0, 0, objects, hAlign='CENTER', vAlign='TOP')
        self.Story.append(inframe)


    ''' 
        Functions for working with images
    '''
    def put_photo(self, filename, width=0, height=0):
        image = self.get_photo(filename, width, height)
        self.Story.append(image)

    def get_photo(self, file_, width=0, height=0):
        if hasattr(file_, 'name'):
            if str(file_.name).rsplit('.', 1)[1].lower() == 'pdf':
                max_height = self.full_height - 2.4 * cm
                f = self.get_file(file_)
                image = PdfImage(f, height=max_height/1.2)
            else:
                image = self.fetch_image(file_, width, height)
        else:
            image = self.fetch_static_image(file_, width, height)
        image.hAlign = 'CENTER'
        return image

    def get_file(self, file_obj):
        MEDIA_ROOT = environ.Path(settings.MEDIA_ROOT)
        file_ = str(MEDIA_ROOT.path(str(file_obj.name)))
        return file_

    def fetch_image(self, image, width=0, height=0):
        file_ = self.get_file(image)
        return self.proc_image(file_, width, height)

    def fetch_static_image(self, img, width=0, height=0):
        file_ = str(settings.APPS_DIR.path('static', 'src', 'assets', 'images', img))
        return self.proc_image(file_, width, height)

    def proc_image(self, file_, width=0, height=0):
        image = PILImage.open(file_)
        max_width = self.full_width
        max_height = self.full_height
        maxsize = (
            (width * cm or max_width), 
            (height * cm or max_height - 2.4 * cm)
        )
        # Get new image dimensions to fit in desired size
        image.thumbnail(maxsize, PILImage.ANTIALIAS)
        w, h = Image(file_, width=image.width, height=image.height).wrap(image.width, image.height)
        return Image(file_, width=image.width, height=image.height)

    def read_excel_data(self):
        try:
            file_entry = FileStorage.objects.get(pk=int(self.data['files']['excel'][0]['id']))
        except IndexError:
            return None
        file_ = self.get_file(file_entry.fileupload)
        excel_importer = ExcelImporter()
        header, rows = excel_importer.read(file_)
        values = tuple(map(lambda x: (x[0], x[1]), filter(lambda x: x[1], rows)))
        
        # Group keys with possible multiple values in tuples instead of plain string
        def mapToDict(res, x):
            key, value = x
            if key not in res:
                res[key] = value
            else:
                if isinstance(res[key], str):
                    res[key] = (res[key], value)
                else:
                    res[key] = (*res[key], value)
            return res

        return reduce(mapToDict, values, {})

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
        file_ = str(settings.APPS_DIR.path('static', 'src', 'assets', 'fonts', font_file))
        MyFontObject = ttfonts.TTFont(font_name, file_)
        pdfmetrics.registerFont(MyFontObject)
     
    def setup_styles(self):
        self.styles.add(ParagraphStyle(name='Justify', alignment=TA_CENTER))
        self.styles.add(ParagraphStyle(
            name='Heading 1 Big Bold',
            fontName='Times Bold',
            fontSize=16,
            leading=30,
            alignment=TA_CENTER))
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
            name='Regular Center Tall',
            fontName='Times',
            fontSize=13,
            leading=16,
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
            fontSize=12,
            leading=13,
            leftIndent=88,
            firstLineIndent=-88,
            alignment=TA_LEFT))
        # Container's Report specific styles. Until they lies here
        self.styles.add(ParagraphStyle(
            name='Text',
            fontName='Times',
            fontSize=12,
            leading=18,
            bulletIndent=18,
            firstLineIndent=1.25 * cm,
            alignment=TA_JUSTIFY))
        self.styles.add(ParagraphStyle(
            name='Text Simple',
            fontName='Times',
            fontSize=12,
            leading=16,
            bulletIndent=18,
            alignment=TA_LEFT))
        self.styles.add(ParagraphStyle(
            name='Text Simple Indent',
            fontName='Times',
            fontSize=12,
            leading=18,
            leftIndent=24,
            bulletIndent=3,
            alignment=TA_JUSTIFY))
        self.styles.add(ParagraphStyle(
            name='Text Simple Bold',
            fontName='Times Bold',
            fontSize=12,
            leading=16,
            bulletIndent=18,
            alignment=TA_LEFT))
        self.styles.add(ParagraphStyle(
            name='Text Simple Right',
            fontName='Times',
            fontSize=12,
            leading=16,
            bulletIndent=18,
            alignment=TA_RIGHT))
        self.styles.add(ParagraphStyle(
            name='Text Simple Center',
            fontName='Times',
            fontSize=12,
            leading=16,
            bulletIndent=18,
            alignment=TA_CENTER))
        self.styles.add(ParagraphStyle(
            name='Text Simple Leading Center',
            fontName='Times',
            fontSize=14,
            leading=16,
            alignment=TA_CENTER))
        self.styles.add(ParagraphStyle(
            name='Text Simple Leading',
            fontName='Times',
            fontSize=14,
            leading=24,
            alignment=TA_LEFT))
        self.styles.add(ParagraphStyle(
            name='Text Simple Center Leading',
            fontName='Times',
            fontSize=14,
            leading=22,
            alignment=TA_CENTER))
        self.styles.add(ParagraphStyle(
            name='Text Simple Center Bold',
            fontName='Times Bold',
            fontSize=12,
            leading=16,
            bulletIndent=18,
            alignment=TA_CENTER))
        self.styles.add(ParagraphStyle(
            name='Text Simple Dense',
            fontName='Times',
            fontSize=12,
            leading=14,
            bulletIndent=18,
            alignment=TA_LEFT))
        self.styles.add(ParagraphStyle(
            name='Text Simple Height',
            fontName='Times',
            fontSize=12,
            leading=18,
            #firstLineIndent=-0.40 * cm,
            #bulletIndent=0 * cm,
            #leftIndent=0.40 * cm,
            alignment=TA_JUSTIFY))
        self.styles.add(ParagraphStyle(
            name='Text Simple Center Dense',
            fontName='Times',
            fontSize=12,
            leading=14,
            bulletIndent=18,
            alignment=TA_CENTER))
        self.styles.add(ParagraphStyle(
            name='TOC',
            fontName='Times Bold',
            fontSize=12,
            leading=18,
            firstLineIndent=1.25 * cm,
            bulletFontName='Times',
            bulletFontSize=15,
            bulletIndent=30,
            alignment=TA_LEFT))
        self.styles.add(ParagraphStyle(
            name='TOC Appendix',
            fontName='Times Bold',
            fontSize=12,
            leading=16,
            alignment=TA_CENTER))
        self.styles.add(ParagraphStyle(
            name='TOC Appendix Hidden',
            fontName='Times Bold',
            fontSize=0.1,
            textColor=colors.white,
            alignment=TA_CENTER))
        self.styles.add(ParagraphStyle(
            name='TOC Hidden',
            fontName='Times Bold',
            fontSize=0.1,
            textColor=colors.white,
            alignment=TA_CENTER))
        self.styles.add(ParagraphStyle(
            name='TOC Hidden wo dots',
            fontName='Times Bold',
            fontSize=0.1,
            textColor=colors.white,
            alignment=TA_CENTER))
        self.styles.add(ParagraphStyle(
            name='TOCHeading1',
            fontName='Times Bold',
            fontSize=12,
            leading=16,
            alignment=TA_CENTER))
        self.styles.add(ParagraphStyle(
            name='TOCHeading2',
            fontName='Times',
            fontSize=12,
            leading=18,
            firstLineIndent=-3.25 * cm,
            leftIndent=3.25 * cm,
            alignment=TA_LEFT))
        self.styles.add(ParagraphStyle(
            name='TOCHeading3',
            fontName='Times',
            fontSize=13,
            leading=18,
            #firstLineIndent=-3.25 * cm,
            #leftIndent=3.25 * cm,
            alignment=TA_LEFT))
        self.styles.add(ParagraphStyle(
            name='TOCHeading4',
            #fontName='Times Bold',
            fontName='Times',
            fontSize=13,
            leading=18,
            #firstLineIndent=-3.25 * cm,
            #leftIndent=3.25 * cm,
            alignment=TA_LEFT))
