import sys
import unittest

sys.path.append("src")

from nukleus.Bom import Bom
from nukleus.SexpParser import load_tree
from nukleus.ParserVisitor import ParserVisitor

class TestParserPlot(unittest.TestCase):
    def test_bom(self):
        bom = Bom()
        with open('samples/files/summe_v6/main.kicad_sch', 'r') as f:
            tree = load_tree(f.read())
            parser = ParserVisitor(bom)
            parser.visit(tree)


        res = bom.bom()
        self.assertEqual(1, len(res))
        self.assertEqual(4, len(res['bom']))
        self.assertEqual(['C1', 'C2'], res['bom'][0]['ref'])
