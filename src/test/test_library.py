import unittest

import sys
sys.path.append('src')
sys.path.append('..')

from nukleus.Library import Library

class TestLibrary(unittest.TestCase):
    def test_device_tl072(self):
        lib = Library(['samples/files/symbols'])
        lib_sym = lib.get('Amplifier_Operational:TL072')
        self.assertEqual('TL072', lib_sym.identifier)
        self.assertEqual(3, len(lib_sym.units)) 

