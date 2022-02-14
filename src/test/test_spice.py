import unittest
import os

import sys
sys.path.append('src')
sys.path.append('..')

from nukleus import Schema
import nukleus.Spice as spice
from nukleus import load_schema
import nukleus.Circuit as Circuit

class TestSpice(unittest.TestCase):
    def test_load_spice(self):

        schema = load_schema('samples/files/main/main.kicad_sch')
        nl = spice.netlist(schema)
        cwd = os.getcwd() + '/samples/files/spice'
        models = spice.load_spice_models([cwd])
        circuit = Circuit()
        circuit.models(models)
        spice.schema_to_spice(schema, circuit, nl)
        self.assertEqual(4, len(circuit.netlist))
        self.assertEqual('R3 INPUT 1 100k', circuit.netlist[0].__str__())
        self.assertEqual('R4 1 IN_1 100k', circuit.netlist[1].__str__())
        self.assertEqual('R5 OUTPUT IN_1 1k', circuit.netlist[2].__str__())
        self.assertEqual('XU1 IN_1 1 GND -15V NC NC NC +15V TL072c',
                         circuit.netlist[3].__str__())
