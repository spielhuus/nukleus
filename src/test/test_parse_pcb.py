from typing import List
import unittest

import sys
sys.path.append('src')
sys.path.append('..')

from nukleus.PCB import PCB
from nukleus.ParserV6 import ParserV6

class TestParserV6(unittest.TestCase):

    def test_parse_summe(self):
        pcb = PCB()
        parser = ParserV6()
        parser.pcb(pcb, "samples/files/produkt/main.kicad_pcb")
        self.maxDiff = None
        #with open('new_main.kicad_sch', 'w') as file:
        #    file.write(schema.sexp())
        with open('samples/files/produkt/main.kicad_pcb', 'r') as file:
            orig = file.read()
            self.assertEqual(orig, schema.sexp())