#!/usr/bin/python3
#
# libs.xml.parsing.py
#

import io 

class SimpleXMLParser:
    def __init__(self, handler):
        self.handler = handler
        self.lineNumber = 1

    def next(self):
        self.ch = self.stream.read(1)
        if self.ch == '\n':
            self.lineNumber += 1   

    def parse(self, stream):
        self.stream = stream
        self.next()
        self.process()

    def process(self):
        while self.ch != '':
            if self.ch == '<':
                self.next()
                if self.ch == '?':
                    self.next()
                    if self.ch.isalnum():
                        target = io.StringIO()
                        while self.ch.isalnum():
                            target.write(self.ch)
                            self.next()
                        self.skipWhite()
                        data = io.StringIO()
                        while self.ch != '?':
                            data.write(self.ch)
                            self.next()
                        self.next()
                        if self.ch == '>':
                            self.handler.processingInstruction(target=target.getvalue(), data=data.getvalue())
                            self.next()
                        else:
                            self.unexpectedCharacter()
                    else:
                        self.unexpectedCharacter()
                elif self.ch == '!':
                    self.next()
                    if self.ch == '-':
                        self.next()
                        if self.ch == '-':
                            self.next()
                            text = io.StringIO()
                            while True:
                                if self.ch == '-':
                                    self.next()
                                    if self.ch == '-':
                                        self.next()
                                        if self.ch == '>':
                                            self.next()
                                            break
                                        else:
                                            text.write('--')
                                    else:
                                        text.write('-')
                                else:
                                    text.write(self.ch)
                                    self.next()
                            self.handler.comment(text.getvalue())
                        else:
                            self.unexpectedCharacter()
                    else:
                        self.unexpectedCharacter()
                elif self.ch.isalnum():
                    tag = io.StringIO()
                    while self.ch.isalnum() or self.ch in ':':
                        tag.write(self.ch)
                        self.next()
                    attributes = {}
                    self.skipWhite()
                    if self.ch.isalnum():
                        while self.ch.isalnum():
                            key = io.StringIO()
                            while self.ch.isalnum() or self.ch in ':-':
                                key.write(self.ch)
                                self.next()
                            self.skipWhite()
                            if self.ch == '=':
                                self.next()
                                self.skipWhite()
                                if self.ch == '"' or self.ch == "'":
                                    quote = self.ch
                                    self.next()
                                    value = io.StringIO()
                                    while self.ch != quote:
                                        value.write(self.ch)
                                        self.next()
                                    self.next()
                                    attributes[key.getvalue()] = value.getvalue()
                                    self.skipWhite()
                                else:
                                    self.unexpectedCharacter()
                            else:
                                self.unexpectedCharacter()
                    self.handler.startElement(tag.getvalue(), attributes)
                    if self.ch == '/':
                        self.next()
                        self.handler.endElement(tag.getvalue())
                    if self.ch == '>':
                        self.next()
                    else:   
                        self.unexpectedCharacter()     
                elif self.ch == '/':
                    self.next()
                    tag = io.StringIO()
                    while self.ch != '>':
                        tag.write(self.ch)
                        self.next()
                    self.next()
                    self.handler.endElement(tag.getvalue())
                else:
                    self.unexpectedCharacter()
                self.skipWhite()
            elif self.ch != '>':
                text = io.StringIO()
                while self.ch != '<' and self.ch != '':
                    text.write(self.ch)
                    self.next()
                self.handler.characters(text.getvalue())
            else:       
                self.unexpectedCharacter()
        if self.ch != '':
            raise Exception('end of file expected')

    def skipWhite(self):
        while self.ch.isspace():
            self.next()

    def unexpectedCharacter(self, message=None):
        print(self.stream.read(20))
        raise Exception(f'unexpected character {message} {repr(self.ch)} at line {self.lineNumber}')

class Handler:
    def processingInstruction(self, target, data):
        print("PI:", target, data)
    def comment(self, text):
        print("COMMENT:", text)
    def startElement(self, name, attrs):
        print("START:", name, "ATTRS:", attrs)
    def endElement(self, name):
        print("END:", name)
    def characters(self, text):
        print("TEXT:", text)

if __name__ == '__main__':
    xml = """<?xml version="1.0" standalone="yes"?>
<!--comment-->
<root attr1="v1" attr2='v2'>
    <?run version="1.2"?>
    <aaa:child id="c1">hello</aaa:child>
</root>
"""

    parser = SimpleXMLParser(Handler())
    parser.parse(io.StringIO(xml))

