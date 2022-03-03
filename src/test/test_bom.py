import sys
import unittest

from pprint import pprint

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
        pprint(res)
        self.assertEqual(6, len(res))
