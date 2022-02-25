#!/usr/bin/env python3

import math
import sys
import unittest
from unittest.mock import mock_open, patch

import numpy as np

sys.path.append("src")

from nukleus.model import Wire
from nukleus.ParserV6 import ParserV6
from nukleus.Plot import ElementFactory, NodeWire, plot
# from elektron._utils import _pos
from nukleus.Schema import Schema


class TestParserPlot(unittest.TestCase):
    def test_factory(self):
        schema = Schema()
        schema.append(Wire())
        factory = ElementFactory(schema)
        self.assertEqual(NodeWire, type(factory.nodes[0]))
        self.assertEqual(1, len(factory.nodes))

#    def test_plot(self):
#        schema = Schema()
#        parser = ParserV6()
#        parser.schema(schema, "samples/files/summe_v6/main.kicad_sch")
#
#        factory = ElementFactory(schema)
#        self.assertEqual(69, len(factory.nodes))
#        self.assertEqual(14, len([x for x in factory.nodes if isinstance(x, NodeWire)]))
#
#
#    def test_coord(self):
#        schema = Schema()
#        parser = ParserV6()
#        parser.schema(schema, "samples/files/summe_v6/main.kicad_sch")
#
#        factory = ElementFactory(schema)
#        coords = factory.dimension()
#
#        self.assertEqual(53.34, coords[0])
#        self.assertEqual(33.02, coords[1])
#        self.assertEqual(115.57, coords[2])
#        self.assertEqual(163.83, coords[3])
    
    def test_draw(self):
        schema = Schema()
        parser = ParserV6()
        parser.schema(schema, "samples/files/summe_v6/main.kicad_sch")

        plot(schema)

#    def test_pts(self):
#
#        path = [[-2.54, -7.62], [-2.54, -3.81]]
#        pos = [106.68, 156.21]
#        angle = float(0)
#        res = [[104.14, 163.83], [104.14, 160.02]]
#
#        verts = _pos(pos, path, angle, '')
#        self.assertTrue((res == verts).all())
#
#    def test_pts_rot(self):
#
#        path = [[0., 0.], [0., 1.27], [0.762, 1.27],
#                [0., 2.54], [-0.762, 1.27], [0., 1.27]]
#        pos = [93.98, 163.83]
#        res = np.array([[93.98, 163.83], [93.98, 165.1], [93.218, 165.1],
#               [93.98, 166.37], [94.742, 165.1], [93.98, 165.1]])
#        angle = float(180)
#
#        verts = _pos(pos, path, angle, '')
#        self.assertTrue(len(res) == len(verts))
#        self.assertTrue((res == verts).all())
