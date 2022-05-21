from os import wait
import sys
import unittest

from nukleus.AbstractNetlist import AbstractNetlist

sys.path.append("src")
sys.path.append("../src")

import nukleus
from nukleus.ModelBase import *
from nukleus.ModelSchema import *
from nukleus.Schema import Schema
from nukleus.Circuit import Circuit
from nukleus.SpiceModel import load_spice_models
from nukleus.draw.Draw import Draw
from nukleus.draw.Element import Element
from nukleus.draw.Label import Label
from nukleus.draw.Line import Line
from nukleus.ParserVisitor import ParserVisitor
from nukleus.SexpParser import load_tree

class TestNetlist(unittest.TestCase):
    def test_nodes(self):
        draw = Draw(library_path=['samples/files/symbols'])
        draw.add(Line())
        draw.add(Line().up())
        draw.add(Line().left())
        netlist = AbstractNetlist()
        draw.produce(netlist)
        self.assertEqual(4, len(netlist.nets))
        #test that all nets are the same
        iterator = iter(netlist.nets.values())
        first = next(iterator)
        self.assertTrue(all(first == x for x in iterator))

    def test_pins(self):
        draw = Draw(library_path=['samples/files/symbols'])
        draw.add(Line())
        draw.add(Line().up())
        draw.add(Line().left())


        draw.add(Element("+15V", "power:+15V"))
        draw.add(Line().down())
        draw.add(Line().left())

        netlist = AbstractNetlist()
        draw.produce(netlist)
        self.assertEqual(5, len(netlist.nets))
        net = netlist.nets[(17.46, 20.0)]
        self.assertEqual('+15V', net.identifier)

    def test_nodes_power_gnd(self):
        draw = Draw(library_path=['samples/files/symbols'])
        draw.add(Line())
        draw.add(Line().up())
        draw.add(Line().left())


        draw.add(Element("GND", "power:GND"))
        draw.add(Line().down())
        draw.add(Line().left())

        netlist = AbstractNetlist()
        draw.produce(netlist)
        self.assertEqual(5, len(netlist.nets))
        net = netlist.nets[(20.0, 17.46)]
        self.assertEqual('GND', net.identifier)

    def test_nodes_named_power(self):
        draw = Draw(library_path=['samples/files/symbols'])
        draw.add(Line())
        draw.add(Line().up())
        draw.add(Line().left())

        draw.add(Element("GND", "power:GND"))
        draw.add(Line().down())
        draw.add(Line().left())

        netlist = AbstractNetlist()
        draw.produce(netlist)

        self.assertEqual(5, len(netlist.nets))
        net = netlist.nets[(17.46, 20.0)]
        self.assertEqual('GND', net.identifier)

    def test_nodes_named_label(self):
        draw = Draw(library_path=['samples/files/symbols'])
        draw.add(Line())
        draw.add(Line().up())
        draw.add(Line().left())

        draw.add(Label("OUTPUT"))
        draw.add(Line().down())
        draw.add(Line().left())

        netlist = AbstractNetlist()
        draw.produce(netlist)
        self.assertEqual(5, len(netlist.nets))
        net = netlist.nets[(17.46, 20.0)]
        self.assertEqual('OUTPUT', net.identifier)

    def test_netlist(self):
        with open('samples/files/summe_v6/main.kicad_sch') as f:
            tree = load_tree(f.read())
            schema = Schema()
            parser = ParserVisitor(schema)
            parser.visit(tree)

            netlist = AbstractNetlist()
            schema.produce(netlist)

            self.assertEqual(28, len(netlist.nets))
            net = netlist.nets[(96.52, 45.72)]
            self.assertEqual('IN_1', net.identifier)
            net = netlist.nets[(80.01, 50.8)]
            self.assertEqual('GND', net.identifier)

        #subax1 = plt.subplot(121)
        #nx.draw(netlist.graph, with_labels=True, font_weight='bold')
        #plt.show()

    def test_no_connect(self):
        with open('samples/files/summe_v6/main.kicad_sch') as f:
            tree = load_tree(f.read())
            schema = Schema()
            parser = ParserVisitor(schema)
            parser.visit(tree)

            netlist = AbstractNetlist()
            schema.produce(netlist)
            self.assertEqual(3, len(netlist.no_connect))

    def test_spice(self):
        with open('samples/files/summe_v6/main.kicad_sch') as f:
            tree = load_tree(f.read())
            schema = Schema()
            parser = ParserVisitor(schema)
            parser.visit(tree)

            nukleus.set_spice_path(['samples/files/spice'])
            circuit = Circuit()
            schema.produce(circuit)
            self.assertEqual(3, len(circuit.no_connect))

    def test_load_spice(self):
        with open('samples/files/summe_v6/main.kicad_sch') as f:
            tree = load_tree(f.read())
            schema = Schema()
            parser = ParserVisitor(schema)
            parser.visit(tree)

            circuit = Circuit()
            schema.produce(circuit)

            nukleus.set_spice_path(['samples/files/spice'])
            self.assertEqual(4, len(circuit.netlist))
            self.assertEqual('R3 1 INPUT 100k', circuit.netlist[1].__str__())
            self.assertEqual('R4 IN_1 1 100k', circuit.netlist[2].__str__())
            self.assertEqual('R5 IN_1 OUTPUT 1k', circuit.netlist[0].__str__())
            self.assertEqual('XU1 IN_1 1 GND -15V NC NC NC +15V TL072c',
                             circuit.netlist[3].__str__())
