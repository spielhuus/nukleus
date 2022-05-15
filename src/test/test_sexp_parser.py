import sys

sys.path.append('src')
sys.path.append('../src')

import unittest

from nukleus.SexpParser import *


class TestSexpParser(unittest.TestCase):

    def test_parse_pos(self):
        res = load_tree('(at 10 10 0.0)')
        self.assertTrue(isinstance(res, SexpNode))
        self.assertEqual((10.0, 10.0), res.pos())

    def test_get_string(self):
        res = load_tree('(at position 10 0.0)')
        self.assertTrue(isinstance(res, SexpNode))
        self.assertEqual('position', res.get(1, 'POSITION'))

    def test_get_float(self):
        res = load_tree('(at 10 10 0.0)')
        self.assertTrue(isinstance(res, SexpNode))
        self.assertEqual(10.0, res.get(1, 0.0))

    def test_contains(self):
        res = load_tree('(bla (at 10 10 0.0))')
        self.assertTrue('at' in res)
        self.assertFalse('pos' in res)

    def test_get_node(self):
        res = load_tree('(a (b (c d) (e f (subtree 1 2 3))) (g h))')
        self.assertTrue(isinstance(res['b'][0], SexpNode))
        self.assertTrue(isinstance(res['b'][0]['c'][0], SexpNode))
        self.assertEqual('d', res['b'][0]['c'][0].get(1, ''))

    def test_parse(self):
        res = load_tree('(a (b (c d) (e f (subtree 1 2 3))) (g h))')
        self.assertEqual(4, len(res['b'][0]['e'][0]['subtree'][0]))
        self.assertEqual(['1', '2', '3'], res['b'][0]['e'][0]['subtree'][0].values()[1:])

    def test_file(self):
        with open("samples/files/main/main.kicad_sch", "r") as file:
            res = load_tree(file.read())
            self.assertEqual(14, len(res['wire']))

#    def test_visit(self):
#        with open("samples/files/main/main.kicad_sch", "r") as file:
#            res = load_tree(file.read())
#            visitor = SexpVisitor()
#            visitor.visit(res)
#            #aself.assertEqual(14, len(res['wire']))
