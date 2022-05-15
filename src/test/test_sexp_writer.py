from io import StringIO
from sys import path
from typing import ByteString
import unittest
from unittest.mock import patch

import sys
from nukleus.PCB import PCB

from nukleus.SexpWriter import SexpWriter
sys.path.append('src')
sys.path.append('../../src')

from nukleus.Schema import Schema
from nukleus.ModelBase import *
from nukleus.ModelSchema import *
from nukleus.ParserVisitor import ParserVisitor
from nukleus.SexpParser import *


class TestSexpWriter(unittest.TestCase):

    def test_parse_summe(self):
        with open('samples/files/summe_v6/main.kicad_sch', 'r') as infile:
            schema_tree = load_tree(infile.read())
            schema = Schema()
            visitor = ParserVisitor(schema)
            visitor.visit(schema_tree)
            writer = SexpWriter()
            schema.produce(writer)
            self.maxDiff = None
            with open('samples/files/summe_v6/main.kicad_sch', 'r') as file:
                orig = file.read()
                text = "".join([s for s in orig.splitlines(True) if s.strip("\r\n")])
                result = "".join([s for s in str(writer).splitlines(True) if s.strip("\r\n")])
                result += "\n"
                self.assertEqual(text, result)

    def test_parse_produkt_schema(self):
        with open('samples/files/produkt/main.kicad_sch', 'r') as infile:
            schema_tree = load_tree(infile.read())
            schema = Schema()
            visitor = ParserVisitor(schema)
            visitor.visit(schema_tree)
            writer = SexpWriter()
            schema.produce(writer)
            with open('samples/files/produkt/main.kicad_sch', 'r') as file:
                orig = file.read()
                text = "".join([s for s in orig.splitlines(True) if s.strip("\r\n")])
                result = "".join([s for s in str(writer).splitlines(True) if s.strip("\r\n")])
                result += "\n"
                self.assertEqual(text, result)

    def test_parse_produkt_pcb(self):
        with open('samples/files/produkt/main.kicad_pcb', 'r') as infile:
            schema_tree = load_tree(infile.read())
            schema = PCB()
            visitor = ParserVisitor(schema)
            visitor.visit(schema_tree)
            writer = SexpWriter()
            schema.produce(writer)
            self.maxDiff = None
            with open('samples/files/produkt/main.kicad_pcb', 'r') as file:
                orig = file.read()
                text = "".join([s for s in orig.splitlines(True) if s.strip("\r\n")])
                result = "".join([s for s in str(writer).splitlines(True) if s.strip("\r\n")])
                result += "\n"
                self.assertEqual(text, result)
