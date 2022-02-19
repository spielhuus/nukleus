import sys
import unittest

sys.path.append('src')
sys.path.append('..')

from nukleus.model.NoConnect import NoConnect
from nukleus.SexpParser import load_tree


class TestNoConnect(unittest.TestCase):

    def test_parse_no_connect(self):
        sexp_str = load_tree(
                """  (no_connect (at 115.57 78.74) (uuid eae0ab9f-65b2-44d3-aba7-873c3227fba7))""")
        no_connect = NoConnect.parse(sexp_str)
        self.assertEqual(
            'eae0ab9f-65b2-44d3-aba7-873c3227fba7', no_connect.identifier)
        self.assertEqual((115.57, 78.74), no_connect.pos)
        self.assertEqual(0, no_connect.angle)

    def test_new_no_connect(self):
        no_connect = NoConnect(pos=(115.57, 78.74),
                    identifier='eae0ab9f-65b2-44d3-aba7-873c3227fba7',
                    angle=0)
        self.assertEqual(
            'eae0ab9f-65b2-44d3-aba7-873c3227fba7', no_connect.identifier)
        self.assertEqual((115.57, 78.74), no_connect.pos)
        self.assertEqual(0, no_connect.angle)

    def test_sexp_no_connect(self):
        sexp_str = load_tree(
                """  (no_connect (at 115.57 78.74) (uuid eae0ab9f-65b2-44d3-aba7-873c3227fba7))""")
        symbol_instance = NoConnect.parse(sexp_str)
        self.assertEqual(
                """  (no_connect (at 115.57 78.74) (uuid eae0ab9f-65b2-44d3-aba7-873c3227fba7))""",
                symbol_instance.sexp())
