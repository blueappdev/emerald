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
        oop = self.session.charToOop(65)
        self.assertEqual(oop, 16668)

    def testDoubleToSmallSouble(self):
        oop = self.session.doubleToSmallDouble(3.14)
        self.assertEqual(oop, 9264444865456394742)

    def testI32ToOop(self):
        oop = self.session.I32ToOop(3)
        self.assertEqual(oop, gemstone.OOP_Three)

    def testOopToChar(self):
        oop = self.session.oopToChar(16668)
        self.assertEqual(oop, 65)

    def testResolveSymbol(self):
        oop = self.session.resolveSymbol('System')
        self.assertEqual(oop, 76033)

    def testExecuteFetchBytes(self):
        result = self.session.executeFetchBytes(self.session, "'Hello','World'")
        self.assertEqual(result, 'HelloWorld')
  
if __name__ == '__main__':
    unittest.main(verbosity=0)
