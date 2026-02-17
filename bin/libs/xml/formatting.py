#!/usr/bin/python3
#
# libs/xml/formatting.py
#

import os, sys, io
sys.path.insert(0, os.path.dirname(__file__))
import parsing

class Node:
    def __init__(self):
        self.children = []
        self.parent = None

    def addChild(self, child):
        self.children.append(child)
        child.parent = self

    def emit(self, *arguments, indent=0, output):
        print('  ' * indent, *arguments, sep='', end='', file=output)

class Document(Node):
    def __init__(self):
        super().__init__()
        self.name = 'Document'

    def emitOn(self, indent, output):
        for each in self.children:
            each.emitOn(indent=indent, output=output)

class Element(Node):
    def __init__(self):
        super().__init__()
        self.text = None

    def emitOn(self, output, indent):
        self.emit("<", self.name, indent=indent, output=output)
        for key, value in self.attributes.items():
            self.emit(' ', key, '="', value, '"', output=output)
        if len(self.children) == 0:
            if self.text is None:
                self.emit('/>\n', output=output)
            else:
                self.emit('>', output=output)
                self.emit(self.text, output=output)
                self.emit('</', self.name, '>\n', output=output)
        else:
            self.emit('>', output=output)
            assert self.text is None, 'text only allowed on leaf nodes'
            self.emit('\n', output=output)
            for each in self.children:
                each.emitOn(indent=indent+1, output=output)
            self.emit('</', self.name, '>\n', indent=indent, output=output)

class Comment(Node):
    def __init__(self, text):
        self.text = text

    def emitOn(self, output, indent):
        self.emit('<!--', self.text, '-->\n', indent=indent, output=output)

class ProcessingInstruction(Node):
    def __init__(self, target, data):
        self.target = target
        self.data = data

    def emitOn(self, output, indent):
        self.emit('<?', self.target, indent=indent, output=output)
        if self.data != '':
            self.emit(' ', self.data, output=output)
        self.emit('?>\n', output=output)

class XMLHandler(parsing.Handler):
    def __init__(self):
        self.current = Document()

    def processingInstruction(self, target, data):
        self.current.addChild(ProcessingInstruction(target, data))

    def comment(self, text):
        self.current.addChild(Comment(text))

    def startElement(self, name, attributes):
        newElement = Element()
        newElement.name = name
        newElement.attributes = attributes
        newElement.text = None
        self.current.addChild(newElement)
        self.current = newElement

    def endElement(self, name):
        self.current = self.current.parent

    def characters(self, str):
        if str.strip() != '':
            self.current.text = str

class XMLFormatter:
    def process(self, input, output):
        handler = XMLHandler()
        parser = parsing.SimpleXMLParser(handler)
        parser.parse(input)
        assert handler.current.parent is None, 'current is not the document'
        self.output = output
        handler.current.emitOn(indent=0, output=self.output)
        return self.output

if __name__ == '__main__':
    xml = """<?xml version="1.0" standalone="yes"?>
<root attr1="v1" attr2='v2'>
    <?run version="1.2"?>
<!--comment-->
    <child id="c1">hello</child>
</root>
"""

    XMLFormatter().process(io.StringIO(xml), sys.stdout)

