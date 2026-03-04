#!/usr/bin/python3
#
# extractexcel
#
# Extract raw data from excel, disregarding all formatting
#

import sys, zipfile, os, os.path, shutil, xml.sax, re
from datetime import datetime, timedelta

class Extractor:
    def __init__(self, filename):
        self.currentFilename = filename

    def warn(self, *messages):
        print(*messages)

    def error(self, *messages):
        self.warn(*messages)
        sys.exit(2)

    def process(self):
        #print('Process', self.currentFilename)
        self.currentRootName, extension = os.path.splitext(self.currentFilename)
        if extension != '.xlsx':
            self.error('Only xlsx files are supported')
        extension = extension[1:]
        self.outputFilename = self.currentRootName + '_' + extension + '_extract.txt'
        self.unzippedDirectory = self.currentRootName + '_unzipped'
        self.unzipCurrentFilename()
        self.processUnzipped()

    def unzipCurrentFilename(self):
        if os.path.exists(self.unzippedDirectory):
            shutil.rmtree(self.unzippedDirectory)
        with zipfile.ZipFile(self.currentFilename, 'r') as zip:
            zip.extractall(os.path.join(self.unzippedDirectory))

    def processUnzipped(self):
        with open(self.outputFilename, 'w') as self.outputStream:
            self.loadWorkbook()
            self.loadSharedStrings()
            self.loadStyleSheet()
            self.processWorksheetFiles()
        shutil.rmtree(self.unzippedDirectory)

    def loadWorkbook(self):
        file = os.path.join(self.unzippedDirectory, 'xl', 'workbook.xml')
        handler = WorkbookHandler()
        if os.path.exists(file):
            xml.sax.parse(file, handler)
        self.sheetNames = handler.sheetNames

    def loadSharedStrings(self):
        file = os.path.join(self.unzippedDirectory, 'xl', 'sharedStrings.xml')
        handler = SharedStringsHandler()
        if os.path.exists(file):
            xml.sax.parse(file, handler)
        self.sharedStrings = handler.sharedStrings
        #self.warn('Number of shared strings:', len(self.sharedStrings))

    def loadStyleSheet(self):
        file = os.path.join(self.unzippedDirectory, 'xl', 'styles.xml')
        handler = StyleSheetHandler()
        xml.sax.parse(file, handler)
        self.numberFormats = handler.numberFormats
        self.cellFormats = handler.cellFormats       # formerly “cell_formats”
        #print('Number of number formats:', len(self.numberFormats))
        #print('Number of cell formats:', len(self.cellFormats))

    def processWorksheetFiles(self):
        directory = os.path.join(self.unzippedDirectory, 'xl', 'worksheets')
        for file, sheetName in zip(os.listdir(directory), self.sheetNames):
            print('Sheet', sheetName, file=self.outputStream)
            inputFile = os.path.join(directory, file)
            root, extension = os.path.splitext(file)
            self.processWorksheetFile(inputFile)

    def processWorksheetFile(self, inputFile):
        handler = WorksheetHandler(self.outputStream, self.sharedStrings, self.numberFormats, self.cellFormats)
        xml.sax.parse(inputFile, handler)

class WorksheetHandler(xml.sax.handler.ContentHandler):
    def __init__(self, stream, sharedStrings, numberFormats, cellFormats):
        super().__init__()
        self.names = []
        self.stream = stream
        self.sharedStrings = sharedStrings
        self.numberFormats = numberFormats
        self.cellFormats = cellFormats
        self.inCellElement = False
        self.inValueElement = False
        self.inFormulaElement = False
        self.cellHasFormula = False
        self.unusedElements = ['worksheet', 'dimension', 'sheetViews', 'sheetView',
                'sheetFormatPr', 'sheetData', 'pageMargins', 'mergeCells', 'mergeCell']

    def startDocument(self):
        self.currentRowNumber = 1

    def startElement(self, name, attributes):
        #print('startElement', name)
        self.names.append(name)
        if name in self.unusedElements:
            pass
        elif name == 'row':
            self.startRowElement(attributes)
        elif name == 'c':
            self.startCellElement(attributes)
        elif name == 'f':
            self.startFormulaElement(attributes)
        elif name == 'v':
            self.startValueElement(attributes)
        else:
            raise Exception('unsupported start element', name)

    def endElement(self, name):
        #print('endElement', name)
        if name in self.unusedElements:
            pass
        elif name == 'row':
            self.endRowElement()
        elif name == 'c':
            self.endCellElement()
        elif name == 'f':
            self.endFormulaElement()
        elif name == 'v':
            self.endValueElement()
        else:
            raise Exception('unsupported end element', name)
        assert self.names.pop() == name

    def startRowElement(self, attributes):
        self.currentRow = []
        self.currentColumnNumber=1
        self.rowSpanBegin = None
        self.rowSpanEnd = None
        for key, value in attributes.items():
            if key == 'r':
                rowNumber = int(value)
                #print('rowNumber', rowNumber, self.currentRowNumber)
                assert rowNumber >= self.currentRowNumber
                for i in range(self.currentRowNumber, rowNumber):
                    self.emitCurrentRow()
                    self.currentRowNumber += 1
                assert rowNumber == self.currentRowNumber
            elif key == 'spans':
                self.rowSpanBegin, self.rowSpanEnd = [int(each) for each in value.split(':')]
            elif key in ['ht', 'customHeight']:
                pass
            else:
                raise Exception(f'unexpected row attribute {key}={value}')
        assert self.rowSpanBegin is not None
        assert self.rowSpanEnd is not None
        assert self.rowSpanEnd > self.rowSpanBegin
      
    def endRowElement(self):
        #print('endRowElement', self.rowSpanEnd, self.currentRow, self.currentColumnNumber)
        assert self.currentColumnNumber-1 <= self.rowSpanEnd
        for i in range(self.currentColumnNumber-1, self.rowSpanEnd):
            self.appendCell(None)
        self.emitCurrentRow()
        self.currentRowNumber += 1

    def startCellElement(self, attributes):
        self.currentCellType = None
        self.currentCellReference = None
        self.currentCellStyleNumber = None
        self.inCellElement = True
        self.currentValue = None
        self.currentFormula = None
        for key, value in attributes.items():
            # r=A1, s=4 (pointer for styles), t=s (type=str)
            if key == 't':
                self.currentCellType = value
            elif key == 'r':
                self.currentCellReference = value
            elif key == 's':
                self.currentCellStyleNumber = value
            else:
                raise Exception(f'unexpected cell attribute {key}={value}')
        rowNumber, columnNumber = self.splitCellReference(self.currentCellReference)
        #print(self.currentCellReference, rowNumber, columnNumber, self.currentColumnNumber)
        assert columnNumber >= self.currentColumnNumber
        for i in range(self.currentColumnNumber, columnNumber):
            self.appendCell(None)
        assert columnNumber == self.currentColumnNumber

    def endCellElement(self):
        #print('endCell', self.currentValue, self.currentCellType)
        if self.isStringCell():
            assert self.currentFormula is None
            value = self.sharedStrings[int(self.currentValue)]
        elif self.isBooleanCell():
            assert self.currentFormula is None
            if self.currentValue == '1':
                value = 'TRUE'
            elif self.currentValue == '0':
                value = 'FALSE'
            else:
                raise Exception('unexpected boolean value {self.currentValue}')
        elif self.isDateCell():
            assert self.currentFormula is None
            value = self.formatAsDate(float(self.currentValue))
        else:
            if self.currentFormula is None:
                value = self.currentValue
            else:
                value = '='+self.currentFormula
        self.appendCell(value)
        self.inCellElement = False

    def startValueElement(self, attributes):
        self.inValueElement = True

    def endValueElement(self):
        self.inValueElement = False

    def startFormulaElement(self, attributes):
        self.inFormulaElement = True
    
    def endFormulaElement(self):
        self.inFormulaElement = False

    def isStringCell(self):
        return self.currentCellType == 's'
    
    def isBooleanCell(self):
        return self.currentCellType == 'b'
    
    def isDateCell(self):
        if self.currentCellStyleNumber is None:
            return False
        styleIndex = int(self.currentCellStyleNumber)
        if styleIndex >= len(self.cellFormats):
            return False
        cellFormat = self.cellFormats[styleIndex]
        numFmtId = cellFormat.get('numFmtId')
        if numFmtId is None:
            return False
        # check built‑in date format IDs (14–22, 45–47) or custom format code
        if numFmtId in (14, 15, 16, 17, 18, 19, 20, 21, 22, 45, 46, 47):
            return True
        # check custom format code for date patterns
        if numFmtId in self.numberFormats:
            code = self.numberFormats[numFmtId]
            # require all of y, m, d to be present in the format code
            return all(c in code.lower() for c in ('y', 'm', 'd'))
        return False

    def formatAsDate(self, excelDateNum):
        # Excel dates are days since 1900-01-01 (with a leap-year bug)
        baseDate = datetime(1900, 1, 1)
        # adjust for Excel's leap-year bug (1900 is not a leap year)
        if excelDateNum > 59:
            excelDateNum -= 1
        delta = timedelta(days=excelDateNum - 1)
        dateObj = baseDate + delta
        return dateObj.strftime('%Y-%m-%d')

    def characters(self, str):
        #print('characters', repr(str))
        if self.inValueElement:
            assert self.currentValue is None
            self.currentValue = str
        elif self.inFormulaElement:
            assert self.currentFormula is None
            self.currentFormula = str
        else:
            assert str.isspace(), self.names

    def splitCellReference(self, str):
        match_result = re.fullmatch(r'([A-Z]+)(\d+)', str)
        if match_result is None:
            raise Exception(f'invalid reference {str}')
        letters, digits = match_result.groups()
        return (int(digits), self.letters_to_number(letters))

    def letters_to_number(self, text):
        value = 0
        for ch in text:
            value = value * 26 + (ord(ch) - ord('A') + 1)
        return value

    def emitCurrentRow(self):
        first = True
        #print(f'Emit row with {len(self.currentRow)} cells {self.currentRow}.')
        for each in self.currentRow:
            if first:
                first = False
            else:
                self.emit('\t')
            self.emit(self.getString(each))
        self.emit('\n')

    def emit(self, str):
        self.stream.write(str)

    def getString(self, value):
        if value is None:
            return ''
        return str(value)

    def appendCell(self, value):
        self.currentRow.append(value)
        self.currentColumnNumber += 1


class SharedStringsHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        self.sharedStrings = []
        self.inTextElement = False

    def startElement(self, name, attributes):
        if name == 't':
            self.startTextElement()

    def endElement(self, name):
        if name == 't':
            self.endTextElement()

    def startTextElement(self):
        self.inTextElement = True
        self.currentString = None

    def endTextElement(self):
        assert self.currentString is not None
        self.sharedStrings.append(self.currentString)
        self.inTextElement = False

    def characters(self, str):
        if self.inTextElement:
            assert self.currentString is None
            self.currentString = str
        else:
            assert str.isspace()

class StyleSheetHandler(xml.sax.handler.ContentHandler):
    def startDocument(self):
        self.numberFormats = {}
        self.cellFormats = []            # accumulate <xf> attribute dictionaries
        self.inCellFormatsElement = False

    def startElement(self, name, attributes):
        if name == 'numFmt':
            self.startNumberFormat(attributes)
        elif name == 'cellXfs':          # <cellXfs> contains the cell-format records
            self.inCellFormatsElement = True
        elif name == 'xf':               # Ignore other <xf> elements
            if self.inCellFormatsElement:
                self.startCellFormatElement(attributes)

    def endElement(self, name):
        if name == 'cellXfs':
            self.inCellFormatsElement = False

    def startCellFormatElement(self, attributes):
        rec = {}
        for k, v in attributes.items():
            rec[k] = int(v) if v.isdigit() else v
        self.cellFormats.append(rec)

    def startNumberFormat(self, attributes):
        numid = attributes.get('numFmtId')
        code = attributes.get('formatCode')
        if numid is not None and code is not None:
            self.numberFormats[int(numid)] = code

class WorkbookHandler(xml.sax.handler.ContentHandler):
    def startDocument(self):
        self.sheetNames = [] 

    def startElement(self, name, attributes):
        if name == 'sheet':
            self.startSheetElement(attributes)

    def endElement(self, name):
        pass

    def startSheetElement(self, attributes):
        #print(attributes.get('name'))
        self.sheetNames.append(attributes.get('name'))


