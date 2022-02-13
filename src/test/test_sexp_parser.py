import sys
sys.path.append('src')

import unittest

from nukleus.SexpParser import load_tree


class TestSexpParser(unittest.TestCase):

    def test_file(self):
        with open("samples/files/main/main.kicad_sch", "r") as file:
            res = load_tree(file.read())
            self.assertEqual(52, len(res))
            self.assertEqual(['version', '20211123'], res[1])
