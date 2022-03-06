import sys
import unittest

sys.path.append("src")

from nukleus.ParserV6 import ParserV6
from nukleus.Schema import Schema
from nukleus.Bom import bom

class TestParserPlot(unittest.TestCase):
    def test_draw(self):
        schema = Schema()
        parser = ParserV6()
        parser.schema(schema, "samples/files/summe_v6/main.kicad_sch")

        res = bom(schema)
        self.assertEqual(1, len(res))
        self.assertEqual(4, len(res['bom']))
        self.assertEqual(['C1', 'C2'], res['bom'][0]['ref'])
