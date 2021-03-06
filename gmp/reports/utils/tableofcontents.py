#Copyright ReportLab Europe Ltd. 2000-2004
#see license.txt for license details
#history http://www.reportlab.co.uk/cgi-bin/viewcvs.cgi/public/reportlab/trunk/reportlab/platypus/tableofcontents.py

__version__=''' $Id: tableofcontents.py 3702 2010-04-14 17:13:41Z rgbecker $ '''
__doc__="""Experimental class to generate Tables of Contents easily

This module defines a single TableOfContents() class that can be used to
create automatically a table of tontents for Platypus documents like
this:

    story = []
    toc = TableOfContents()
    story.append(toc)
    # some heading paragraphs here...
    doc = MyTemplate(path)
    doc.multiBuild(story)

The data needed to create the table is a list of (level, text, pageNum)
triplets, plus some paragraph styles for each level of the table itself.
The triplets will usually be created in a document template's method
like afterFlowable(), making notification calls using the notify()
method with appropriate data like this:

    (level, text, pageNum) = ...
    self.notify('TOCEntry', (level, text, pageNum))

Optionally the list can contain four items in which case the last item
is a destination key which the entry should point to. A bookmark
with this key needs to be created first like this:

    key = 'ch%s' % self.seq.nextf('chapter')
    self.canv.bookmarkPage(key)
    self.notify('TOCEntry', (level, text, pageNum, key))

As the table of contents need at least two passes over the Platypus
story which is why the moultiBuild0() method must be called.

The level<NUMBER>ParaStyle variables are the paragraph styles used
to format the entries in the table of contents. Their indentation
is calculated like this: each entry starts at a multiple of some
constant named delta. If one entry spans more than one line, all
lines after the first are indented by the same constant named
epsilon.
"""
from json import loads, JSONDecodeError

from reportlab.lib import enums
from reportlab.lib.units import cm
from reportlab.lib.utils import commasplit, escapeOnce
from reportlab.lib.styles import ParagraphStyle, _baseFontName
from reportlab.platypus.paragraph import Paragraph
from reportlab.platypus.doctemplate import IndexingFlowable
from reportlab.platypus.tables import TableStyle, Table
from reportlab.platypus.flowables import Spacer, Flowable
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from base64 import encodestring, decodestring

#try:
#    import cPickle as pickle
#except ImportError:
#    import pickle
#dumps = pickle.dumps
#loads = pickle.loads

def unquote(txt):
    from xml.sax.saxutils import unescape
    return unescape(txt, {"&apos;": "'", "&quot;": '"'})

try:
    set
except:
    class set(list):
        def add(self,x):
            if x not in self:
                list.append(self,x)

def drawPageNumbers(canvas, style, pages, availWidth, availHeight, dot=' . '):
    '''
    Draws pagestr on the canvas using the given style.
    If dot is None, pagestr is drawn at the current position in the canvas.
    If dot is a string, pagestr is drawn right-aligned. If the string is not empty,
    the gap is filled with it.
    '''
    pages.sort()
    pagestr = ', '.join([str(p) for p, _ in pages])
    x, y = canvas._curr_tx_info['cur_x'], canvas._curr_tx_info['cur_y']
    
    fontSize = style.fontSize
    pagestrw = stringWidth(pagestr, style.fontName, fontSize)
    
    #if it's too long to fit, we need to shrink to fit in 10% increments.
    #it would be very hard to output multiline entries.
    #however, we impose a minimum size of 1 point as we don't want an
    #infinite loop.   Ultimately we should allow a TOC entry to spill
    #over onto a second line if needed.
    freeWidth = availWidth-x
    while pagestrw > freeWidth and fontSize >= 1.0:
        fontSize = 0.9 * fontSize
        pagestrw = stringWidth(pagestr, style.fontName, fontSize)
        
    
    if isinstance(dot, str):
        if dot:
            dotw = stringWidth(dot, style.fontName, fontSize)
            dotsn = int((availWidth-x-pagestrw)/dotw)
        else:
            dotsn = dotw = 0
        text = '%s%s' % (dotsn * dot, pagestr)
        newx = availWidth - dotsn*dotw - pagestrw
        pagex = availWidth - pagestrw
    elif dot is None:
        text = ',  ' + pagestr
        newx = x
        pagex = newx
    else:
        raise TypeError('Argument dot should either be None or an instance of basestring.')

    tx = canvas.beginText(newx, y)
    tx.setFont(style.fontName, fontSize)
    tx.setFillColor(style.textColor)
    tx.textLine(text)
    canvas.drawText(tx)

    commaw = stringWidth(', ', style.fontName, fontSize)
    for p, key in pages:
        if not key:
            continue
        w = stringWidth(str(p), style.fontName, fontSize)
        canvas.linkRect('', key, (pagex, y, pagex+w, y+style.leading), relative=1)
        pagex += w + commaw

# Default paragraph styles for tables of contents.
# (This could also be generated automatically or even
# on-demand if it is not known how many levels the
# TOC will finally need to display...)

delta = 1*cm
epsilon = 0.5*cm

defaultLevelStyles = [
    ParagraphStyle(
        name='Level 0',
        fontName=_baseFontName,
        fontSize=10,
        leading=11,
        firstLineIndent = 0,
        leftIndent = epsilon)]

defaultTableStyle = \
    TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
    ])

class TableOfContents(IndexingFlowable):
    """This creates a formatted table of contents.

    It presumes a correct block of data is passed in.
    The data block contains a list of (level, text, pageNumber)
    triplets.  You can supply a paragraph style for each level
    (starting at zero).
    Set dotsMinLevel to determine from which level on a line of
    dots should be drawn between the text and the page number.
    If dotsMinLevel is set to a negative value, no dotted lines are drawn.
    """

    def __init__(self):
        self.rightColumnWidth = 72
        self.levelStyles = defaultLevelStyles
        self.tableStyle = defaultTableStyle
        self.dotsMinLevel = 1
        self._table = None
        self._entries = []
        self._lastEntries = []

    def beforeBuild(self):
        # keep track of the last run
        self._lastEntries = self._entries[:]
        self.clearEntries()

    def isIndexing(self):
        return 1

    def isSatisfied(self):
        return (self._entries == self._lastEntries)

    def notify(self, kind, stuff):
        """The notification hook called to register all kinds of events.

        Here we are interested in 'TOCEntry' events only.
        """
        if kind == 'TOCEntry':
            self.addEntry(*stuff)

    def clearEntries(self):
        self._entries = []

    def getLevelStyle(self, n):
        '''Returns the style for level n, generating and caching styles on demand if not present.'''
        try:
            return self.levelStyles[n]
        except IndexError:
            prevstyle = self.getLevelStyle(n-1)
            self.levelStyles.append(ParagraphStyle(
                    name='%s-%d-indented' % (prevstyle.name, n),
                    parent=prevstyle,
                    firstLineIndent = prevstyle.firstLineIndent+delta,
                    leftIndent = prevstyle.leftIndent+delta))
            return self.levelStyles[n]

    def addEntry(self, level, text, pageNum, key=None):
        """Adds one entry to the table of contents.

        This allows incremental buildup by a doctemplate.
        Requires that enough styles are defined."""

        assert type(level) == type(1), "Level must be an integer"
        self._entries.append((level, text, pageNum, key))


    def addEntries(self, listOfEntries):
        """Bulk creation of entries in the table of contents.

        If you knew the titles but not the page numbers, you could
        supply them to get sensible output on the first run."""

        for entryargs in listOfEntries:
            self.addEntry(*entryargs)


    def wrap(self, availWidth, availHeight):
        "All table properties should be known by now."

        # makes an internal table which does all the work.
        # we draw the LAST RUN's entries!  If there are
        # none, we make some dummy data to keep the table
        # from complaining
        if len(self._lastEntries) == 0:
            _tempEntries = [(0,'Placeholder for table of contents',0,None)]
        else:
            _tempEntries = self._lastEntries

        def getParagraphStyle(style):
            return ParagraphStyle(
                name=style['name'],
                fontName=style['fontName'],
                fontSize=style['fontSize'],
                leading=style['leading'],
                alignment=style['alignment'])

        def drawTOCEntryEnd(canvas, kind, label):
            '''Callback to draw dots and page numbers after each entry.'''
            label = label.split(',')
            page, level, key, widthMul = int(label[0]), int(label[1]), eval(label[2],{}), float(label[3])
            style = self.getLevelStyle(level)
            if self.dotsMinLevel >= 0 and level >= self.dotsMinLevel:
                dot = ' . '
            else:
                dot = ''
            drawPageNumbers(canvas, style, [(page, key)], availWidth * widthMul, availHeight, dot)
        self.canv.drawTOCEntryEnd = drawTOCEntryEnd

        tableData = []
        for (level, text, pageNum, key) in _tempEntries:
            style = self.getLevelStyle(level)
            # JSON-encoded TOC entry
            try:
                entry = loads(text)
                first_col_width = entry[0]['width']
                last_col_width = entry[1]['width']
                style1 = getParagraphStyle(entry[0]['font'])
                style2 = getParagraphStyle(entry[1]['font'])

                if key:
                    text1 = '<a href="#%s">%s</a>' % (key, entry[0]['text'])
                    text2 = '<a href="#%s">%s</a>' % (key, entry[1]['text'])
                    keyVal = repr(key).replace(',','\\x2c').replace('"','\\x2c')
                else:
                    keyVal = None

                para1 = Paragraph('{}<label="{:d},{:d},{}"/>'.format(
                    text1, pageNum, level, keyVal), style1)
                para2 = Paragraph('{}<onDraw name="drawTOCEntryEnd" label="{:d},{:d},{},{:f}"/>'.format(
                    text2, pageNum, level, keyVal, last_col_width), style2)

                tableData.append([para1, para2])
                widths = (availWidth * first_col_width , availWidth * last_col_width)
            # Plain TOC entry
            except JSONDecodeError:
                if key:
                    text = '<a href="#%s">%s</a>' % (key, text)
                    keyVal = repr(key).replace(',','\\x2c').replace('"','\\x2c')
                else:
                    keyVal = None

                para = Paragraph('{}<onDraw name="drawTOCEntryEnd" label="{:d},{:d},{},{:f}"/>'.format(
                    text, pageNum, level, keyVal, 1), style)

                if style.spaceBefore:
                    tableData.append([Spacer(1, style.spaceBefore),])
                tableData.append([para])
                widths = (availWidth, )

        self._table = Table(tableData, colWidths=widths, style=self.tableStyle)
        #    para = Paragraph('%s<onDraw name="drawTOCEntryEnd" label="%d,%d,%s"/>' % (text, pageNum, level, keyVal), style)
        #    if style.spaceBefore:
        #        tableData.append([Spacer(1, style.spaceBefore),])
        #    tableData.append([
        #        Paragraph('%s<onDraw name="drawTOCEntryEnd" label="%d,%d,%s"/>' % ('Формуляр', pageNum, level, keyVal), style),
        #        para])

        #self._table = Table(tableData, colWidths=(availWidth * .2, availWidth * .8), style=self.tableStyle)

        self.width, self.height = self._table.wrapOn(self.canv,availWidth, availHeight)
        return (self.width, self.height)


    def split(self, availWidth, availHeight):
        """At this stage we do not care about splitting the entries,
        we will just return a list of platypus tables.  Presumably the
        calling app has a pointer to the original TableOfContents object;
        Platypus just sees tables.
        """
        return self._table.splitOn(self.canv,availWidth, availHeight)


    def drawOn(self, canvas, x, y, _sW=0):
        """Don't do this at home!  The standard calls for implementing
        draw(); we are hooking this in order to delegate ALL the drawing
        work to the embedded table object.
        """
        self._table.drawOn(canvas, x, y, _sW)

def makeTuple(x):
    if hasattr(x, '__iter__'):
        return tuple(x)
    return (x,)


def listdiff(l1, l2):
    m = min(len(l1), len(l2))
    for i in range(m):
        if l1[i] != l2[i]:
            return i, l2[i:]
    return m, l2[m:]

class ReferenceText(IndexingFlowable):
    """Fakery to illustrate how a reference would work if we could
    put it in a paragraph."""
    def __init__(self, textPattern, targetKey):
        self.textPattern = textPattern
        self.target = targetKey
        self.paraStyle = ParagraphStyle('tmp')
        self._lastPageNum = None
        self._pageNum = -999
        self._para = None

    def beforeBuild(self):
        self._lastPageNum = self._pageNum

    def notify(self, kind, stuff):
        if kind == 'Target':
            (key, pageNum) = stuff
            if key == self.target:
                self._pageNum = pageNum

    def wrap(self, availWidth, availHeight):
        text = self.textPattern % self._lastPageNum
        self._para = Paragraph(text, self.paraStyle)
        return self._para.wrap(availWidth, availHeight)

    def drawOn(self, canvas, x, y, _sW=0):
        self._para.drawOn(canvas, x, y, _sW)


