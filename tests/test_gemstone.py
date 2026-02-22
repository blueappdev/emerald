#!/usr/bin/python3
#
# test_gemstone.py
#

import os, sys, unittest, configparser

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
LIBS_DIR = os.path.join(ROOT_DIR, 'bin/libs')
if LIBS_DIR not in sys.path:
    sys.path.insert(0, LIBS_DIR)

import gemstone

class GemStoneTests(unittest.TestCase):
    session: gemstone.Session

    @classmethod
    def setUpClass(cls):
        cls.session = gemstone.Session()

        configuration = configparser.ConfigParser()
        configuration.read('conf/test_gemstone.ini')
        gem_host = configuration.get('gemstone', 'gem_host')
        stone = configuration.get('gemstone', 'stone')
        gs_user = configuration.get('gemstone', 'gs_user')
        gs_password = configuration.get('gemstone', 'gs_password')
        netldi = configuration.get('gemstone', 'netldi')
        host_user = configuration.get('gemstone', 'host_user')
        host_password = configuration.get('gemstone', 'host_password')

        cls.session.login(
            gem_host=gem_host,
            stone=stone,
            gs_user=gs_user, 
            gs_password=gs_password, 
            netldi=netldi,
            host_user=host_user,
            host_password=host_password)

    @classmethod
    def tearDownClass(cls):
        cls.session.logout()

    def testIsSessionValid(self):
        result = self.session.isSessionValid()
        self.assertTrue(result)

    def testAbort(self):
        self.session.abort()

    def testBegin(self):
        self.session.begin()

    def testCommit(self):
        self.session.commit()

    def testVersion(self):
        version = self.session.version()
        # Expected: 3.6.2 build 2021-10-22i...
        self.assertTrue(version.startswith('3.6.2'))

    def testOopIsSpecial(self):
        self.assertTrue(self.session.oopIsSpecial(gemstone.OOP_NIL))
        self.assertFalse(self.session.oopIsSpecial(37632513))

    def testCharToOop(self):
        result = self.session.charToOop(65)
        self.assertEqual(result, 16668)

    def testDoubleToSmallDouble(self):
        result = self.session.doubleToSmallDouble(3.14)
        self.assertEqual(result, 9264444865456394742)

    def testI32ToOop(self):
        result = self.session.I32ToOop(3)
        self.assertEqual(result, gemstone.OOP_Three)
        result = self.session.I32ToOop(-2)
        self.assertEqual(result, gemstone.OOP_MinusTwo)

    def testOopToChar(self):
        result = self.session.oopToChar(16668)
        self.assertEqual(result, 65)

    def testResolveSymbol(self):
        result = self.session.resolveSymbol('String')
        self.assertEqual(result, gemstone.OOP_CLASS_STRING)

    def testResolveSymbolObj(self):
        oop = self.session.newString('String')
        result = self.session.resolveSymbolObj(oop)
        self.assertEqual(result, gemstone.OOP_CLASS_STRING)
        oop = self.session.newString('Utf8')
        result = self.session.resolveSymbolObj(oop)
        self.assertEqual(result, gemstone.OOP_CLASS_Utf8)

    def testExecute(self):
        result = self.session.execute("4-6")  # returns an Oop
        self.assertEqual(result, gemstone.OOP_MinusTwo)

    def testExecuteWithUnderscore(self):
        result = self.session.execute_("4-6")  # returns an Oop
        self.assertEqual(result, gemstone.OOP_MinusTwo)

    def testExecuteFetchBytes(self):
        result = self.session.executeFetchBytes("'Hello', ' ', 'World'")
        self.assertEqual(result, 'Hello World')

    def testPerformFetchBytes(self):
        result = self.session.performFetchBytes(gemstone.OOP_Three, 'printString', [])
        self.assertEqual(result, '3')
        result = self.session.performFetchBytes(gemstone.OOP_NIL, 'printString', [])
        self.assertEqual(result, 'nil')

    def testStringConcatenation(self):
        hello = self.session.newString('Hello')
        world = self.session.newString('World')
        result = self.session.performFetchBytes(hello, ',', [world])
        self.assertEqual(result, 'HelloWorld')

    def testPerform1(self):
        result = self.session.perform(gemstone.OOP_One, gemstone.OOP_ILLEGAL, 'yourself', [])
        self.assertEqual(result, gemstone.OOP_One)

    def testPerform2(self):
        result = self.session.perform(gemstone.OOP_One, gemstone.OOP_ILLEGAL, '+', [gemstone.OOP_Two])
        self.assertEqual(result, gemstone.OOP_Three)

    def testNewSymbol(self):
        oop = self.session.newSymbol('printString')
        self.assertEqual(oop, 3362049)

    def testNewString(self):
        string = self.session.newString('printString')
        symbol = self.session.newSymbol('printString')
        self.assertNotEqual(string, symbol)

  
if __name__ == '__main__':
    unittest.main(verbosity=1)
