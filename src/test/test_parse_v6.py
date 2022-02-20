from typing import List
import unittest

import sys
sys.path.append('src')
sys.path.append('..')

from nukleus import Schema
from nukleus.ParserV6 import ParserV6

from nukleus.model import Wire, NoConnect, Junction, LocalLabel, \
    GlobalLabel, LibrarySymbol, Symbol, FillType, \
    Justify, rgb

def get_lines(input: str) -> List[str]:
    return input.split()

class TestParserV6(unittest.TestCase):

    def test_parse_summe(self):
        schema = Schema()
        parser = ParserV6()
        parser.schema(schema, "samples/files/summe_v6/main.kicad_sch")
        self.maxDiff = None
        #with open('new_main.kicad_sch', 'w') as file:
        #    file.write(schema.sexp())
        with open('samples/files/summe_v6/main.kicad_sch', 'r') as file:
            orig = file.read()
            self.assertEqual(orig, schema.sexp())



















#    def test_parse_rectangle(self):
#        parser = ParserV6()
#        res = parser._rectangle(['rectangle',
#                                ['start', -1.016, -2.54], ['end', 1.016, 2.54],
#                                ['stroke', ['width', 0.254],
#                                 ['type', 'default'],
#                                 ['color', 0, 0, 0, 0]],
#                                ['fill', ['type', 'none']]])
#        self.assertEqual(-1.016, res.start_x)
#        self.assertEqual(-2.54, res.start_y)
#        self.assertEqual(1.016, res.end_x)
#        self.assertEqual(2.54, res.end_y)
#        self.assertEqual('default', res.stroke_definition.type)
#        self.assertEqual(FillType.NONE, res.fill)
#
#    def test_parse_points(self):
#        parser = ParserV6()
#        res = parser._pts(['pts', ['xy', 80.01, 33.02], ['xy', 80.01, 43.18]])
#        self.assertEqual(2, len(res))
#        self.assertEqual((80.01, 33.02), res[0])
#        self.assertEqual((80.01, 43.18), res[1])
#
#    def test_parse_stroke(self):
#        parser = ParserV6()
#        res = parser._stroke(['stroke', ['width', 0],
#                             ['type', 'default'],
#                             ['color', 0, 0, 0, 0]])
#        self.assertEqual(rgb(0, 0, 0, 0), res.color)
#        self.assertEqual("default", res.type)
#        self.assertEqual(.0, res.width)
#
#    def test_parse_effects(self):
#        parser = ParserV6()
#        res = parser._effects(['effects',
#                              ['font',
#                                  ['size', 1.27, 1.27]],
#                              ['justify', 'right', 'bottom']])
#        self.assertEqual(1.27, res.font_height)
#        self.assertEqual(1.27, res.font_width)
#        self.assertEqual([Justify.RIGHT, Justify.BOTTOM], res.justify)
#
#    def test_parse_property(self):
#        parser = ParserV6()
#        res = parser._property(['property', 'Datasheet', '~',
#                               ['id', 3], ['at', 93.98, 152.4, 0],
#                               ['effects', ['font', ['size', 1.27, 1.27]],
#                                'hide']])
#        self.assertEqual("Datasheet", res.key)
#        self.assertEqual("~", res.value)
#        self.assertEqual((93.98, 152.4), res.pos)
#        self.assertEqual(3, res.id)
#        self.assertEqual(1.27, res.text_effects.font_height)
#        self.assertEqual(1.27, res.text_effects.font_width)
#        self.assertEqual(True, res.text_effects.hidden)
#
#    def test_parse_schema_title(self):
#        schema = Schema()
#        parser = ParserV6()
#        parser.schema(schema, "samples/files/summe_v6/main.kicad_sch")
#
#        self.assertEqual("2021-05-30", schema.date)
#        self.assertEqual("20211123", schema.version)
#        self.assertEqual("eeschema", schema.generator)
#        self.assertEqual("summe", schema.title)
#        self.assertEqual("schema for pcb", schema.comment_1)
#        self.assertEqual("DC coupled mixer", schema.comment_2)
#        self.assertEqual("", schema.comment_3)
#        self.assertEqual("License CC BY 4.0 - Attribution 4.0 International",
#                         schema.comment_4)
#        self.assertEqual("A4", schema.paper)
#        self.assertEqual("R02", schema.rev)
#        self.assertEqual("cb24efdd-07c6-4317-9277-131625b065ac", schema.uuid)
#
#    def test_parse_schema_junction(self):
#        schema = Schema()
#        parser = ParserV6()
#        parser.schema(schema, "samples/files/summe_v6/main.kicad_sch")
#        junctions = schema.get_elements(Junction)
#        self.assertEqual(5, len(junctions))
#
#        junction = junctions[0]
#        self.assertEqual("5487601b-81d3-4c70-8f3d-cf9df9c63302",
#                         junction.identifier)
#        self.assertEqual(0, junction.diameter)
#        self.assertEqual("0 0 0 0", junction.color)
#        self.assertEqual((93.98, 148.59), junction.pos)
#
#    def test_parse_schema_no_connect(self):
#        schema = Schema()
#        parser = ParserV6()
#        parser.schema(schema, "samples/files/summe_v6/main.kicad_sch")
#        ncs = schema.get_elements(NoConnect)
#        self.assertEqual(3, len(ncs))
#
#        nc = ncs[0]
#        self.assertEqual("2dc54bac-8640-4dd7-b8ed-3c7acb01a8ea",
#                         nc.identifier)
#        self.assertEqual((115.57, 73.66), nc.pos)
#
#    def test_parse_schema_wire(self):
#        schema = Schema()
#        parser = ParserV6()
#        parser.schema(schema, "samples/files/summe_v6/main.kicad_sch")
#
#        self.assertEqual(
#            14,
#            len([x for x in schema.elements if isinstance(x, Wire)]))
#        wires: List[Wire] = schema.get_elements(Wire)
#        self.assertEqual(14, len(wires))
#        self.assertEqual(2, len(wires[0].pts))
#
#        nc = schema.get_elements(NoConnect)
#        self.assertEqual(3, len(nc))
#
#    def test_parse_schema_label(self):
#        schema = Schema()
#        parser = ParserV6()
#        parser.schema(schema, "samples/files/summe_v6/main.kicad_sch")
#
#        self.assertEqual(
#            14,
#            len([x for x in schema.elements if isinstance(x, Wire)]))
#        labels: List[LocalLabel] = schema.get_elements(LocalLabel)
#        self.assertEqual(1, len(labels))
#        # TODO self.assertEqual(2, len(wires[0].pts))
#
#        # nc = parser.get_elements(NoConnect)
#        # self.assertEqual(3, len(nc))
#
#    def test_parse_schema_global_label(self):
#        schema = Schema()
#        parser = ParserV6()
#        parser.schema(schema, "samples/files/summe_v6/main.kicad_sch")
#
#        labels: List[GlobalLabel] = schema.get_elements(GlobalLabel)
#        self.assertEqual(2, len(labels))
#        self.assertEqual('INPUT', labels[0].text)
#        self.assertEqual('input', labels[0].shape)
#
#    def test_parse_schema_symbol(self):
#        schema = Schema()
#        parser = ParserV6()
#        parser.schema(schema, "samples/files/summe_v6/main.kicad_sch")
#
#        self.assertEqual(
#            18,
#            len([x for x in schema.elements if isinstance(x, Symbol)]))
#        symbols: List[Symbol] = schema.get_elements(Symbol)
#        self.assertEqual("Device:R", symbols[0].library_identifier)
#        self.assertEqual((105.41, 45.72), symbols[0].pos)
#        self.assertEqual(90, symbols[0].angle)
#        self.assertEqual('00000000-0000-0000-0000-00005d7bf067', 
#                         symbols[0].identifier)
#
#    def test_parse_schema_library_symbol(self):
#        schema = Schema()
#        parser = ParserV6()
#        parser.schema(schema, "samples/files/summe_v6/main.kicad_sch")
#
##        symbols = parser.get_elements(LibrarySymbol)
##        tl072: List[LibrarySymbol] = [
##            x for x in symbols if x.identifier == 'Amplifier_Operational:TL072']
#        tl072 = schema.getSymbol('Amplifier_Operational:TL072')
#        self.assertEqual(3, len(tl072.units))
#        self.assertEqual(3, len(tl072.units[0].pins))
#        self.assertEqual(3, len(tl072.units[1].pins))
#        self.assertEqual(2, len(tl072.units[2].pins))
#        self.assertEqual(1, len(tl072.units[0].graphics))
#        self.assertEqual(1, len(tl072.units[1].graphics))
#        self.assertEqual(0, len(tl072.units[2].graphics))
#        self.assertEqual('~', tl072.units[0].pins[0].name[0])
#        self.assertEqual(1.27, tl072.units[0].pins[0].name[1].font_height)
#
#    def test_parse_schema_library_gnd(self):
#        schema = Schema()
#        parser = ParserV6()
#        parser.schema(schema, "samples/files/summe_v6/main.kicad_sch")
#
##        symbols = parser.get_elements(LibrarySymbol)
##        tl072: List[LibrarySymbol] = [
##            x for x in symbols if x.identifier == 'Amplifier_Operational:TL072']
#        pwr = schema.getSymbol('power:PWR_FLAG')
#        self.assertEqual('power', pwr.extends)
#
#    def test_get_property_by_name(self):
#        schema = Schema()
#        parser = ParserV6()
#        parser.schema(schema, "samples/files/summe_v6/main.kicad_sch")
#        symbols = schema.get_elements(Symbol)
#        self.assertEqual("Value", symbols[0].property("Value").key)
#
#    def test_references(self):
#        schema = Schema()
#        parser = ParserV6()
#        parser.schema(schema, "samples/files/summe_v6/main.kicad_sch")
#        refs = schema.references()
#        res = ['C1', 'C2', 'R3', 'R4', 'R5', 'U1']
#        self.assertEqual(res, refs)
#
#    def test_reference(self):
#        schema = Schema()
#        parser = ParserV6()
#        parser.schema(schema, "samples/files/summe_v6/main.kicad_sch")
#        sym = schema.R5
#        self.assertEqual('Device:R', sym[1].library_identifier)
#
#    def test_reference_attr(self):
#        schema = Schema()
#        parser = ParserV6()
#        parser.schema(schema, "samples/files/summe_v6/main.kicad_sch")
#        sym = getattr(schema, 'R5')
#        self.assertEqual('Device:R', sym[1].library_identifier)
