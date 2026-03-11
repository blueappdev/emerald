#!/usr/bin/python3
#
# test_xml.py
#

import os, sys, unittest, io

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BIN_DIR = os.path.join(ROOT_DIR, 'bin')
sys.path.insert(0, BIN_DIR)

import libs.xml.formatting

class XMLFormattingTests(unittest.TestCase):

    def testHappyCase(self):
        self.check('<s><a>Hello</a></s>\n', '<s>\n  <a>Hello</a>\n</s>\n')

    def testTrailingSpaces(self):
        self.check('<a>Hello   </a>\n', '<a>Hello   </a>\n')

    def testLeadingSpaces(self):
        self.check('<a>   Hello</a>\n', '<a>   Hello</a>\n')

    def check(self, xml, expected):
        input = io.StringIO(xml)
        output = io.StringIO()
        libs.xml.formatting.XMLFormatter().process(input, output)
        actual = output.getvalue()
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main(buffer=True, verbosity=1)


