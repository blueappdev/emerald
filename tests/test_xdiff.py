#!/usr/bin/python3
#
# test_gemstone.py
#

import os, sys, unittest, configparser

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
from importlib.machinery import SourceFileLoader
xdiff = SourceFileLoader("xdiff", os.path.join(ROOT_DIR, 'bin', 'xdiff')).load_module()

class DiffTests(unittest.TestCase):

    def check(self, left, right, expected):
        viewer = xdiff.DiffViewer(None)
        viewer.ignoreTrailingBlanks = False
        viewer.ignoreAllBlanks = False
        actual=viewer.oneLineDiff(left, right)
        self.assertEqual(actual, expected)

    def testEqual(self):
        self.check('Hello\n', 'Hello\n', (0,0,0,0))

    def testMissingWord(self):
        self.check('Aaa missing theDogJumpsHappily\n', 'Aaa theDogJumpsHappily\n', (4, 20, 4, 20))

    def testMissingSuffix(self):
        self.check('Hello\n', 'Hello World\n', (5, 1, 5, 1))

    def testButter(self):
        self.check('Better\n', 'Butter\n', (1, 5, 1, 5))

    def testSpace(self):
        self.check('aa  bb\n', 'aa  bb\n', (0, 0, 0, 0))
        self.check('aa  bb\n', 'aa   bb\n', (4, 5, 4, 5))

class TrailingBlankTests(unittest.TestCase):
    def check(self, left, right, expected):
        viewer = xdiff.DiffViewer(None)
        viewer.ignoreTrailingBlanks = True
        viewer.ignoreAllBlanks = False
        actual=viewer.oneLineDiff(left, right)
        self.assertEqual(actual, expected)

    def testEqual(self):
        self.check('Hello\n', 'Hello\n', (0,0,0,0))

    def testMissingWord(self):
        self.check('Aaa missing theDogJumpsHappily\n', 'Aaa theDogJumpsHappily\n', (4, 20, 4, 20))

    def testMissingSuffix(self):
        self.check('Hello\n', 'Hello World\n', (5, 1, 5, 1))

    def testButter(self):
        self.check('Better\n', 'Butter\n', (1, 5, 1, 5))

    def testSpace(self):
        self.check('aa  bb\n', 'aa  bb\n', (0, 0, 0, 0))
        self.check('aa  bb\n', 'aa   bb\n', (4, 5, 4, 5))

class AllBlankTests(unittest.TestCase):

    def check(self, left, right, expected):
        viewer = xdiff.DiffViewer(None)
        viewer.ignoreTrailingBlanks = False
        viewer.ignoreAllBlanks = True
        actual=viewer.oneLineDiff(left, right)
        self.assertEqual(actual, expected)

    def testEqual(self):
        self.check('Hello\n', 'Hello\n', (0,0,0,0))

    def testMissingWord(self):
        self.check('Aaa missing theDogJumpsHappily\n', 'Aaa theDogJumpsHappily\n', (4, 20, 4, 20))

    def testMissingSuffix1(self):
        self.check('Hello\n', 'Hello World\n', (5, 1, 5, 1))

    def testMissingSuffix2(self):
        self.check('Hello  \n', 'Hello World      \n', (5, 3, 5, 7))

    def testMissingSuffix3(self):
        self.check('   Hello  \n', '      Hello World      \n', (8, 3, 11, 7))

    def testButter(self):
        self.check('Better\n', 'Butter\n', (1, 5, 1, 5))

    def testSpace(self):
        self.check('aa  bb\n', 'aa  bb\n', (0, 0, 0, 0))
        self.check('aa  bb\n', 'aa   bb\n', (0, 0, 0, 0))

if __name__ == '__main__':
    unittest.main(buffer=True, verbosity=0)


