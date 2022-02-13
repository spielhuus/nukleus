#!/usr/bin/env python3

import numpy as np
import math

import unittest
from unittest.mock import patch, mock_open
import sys
sys.path.append('src')

#from elektron._utils import _pos


#class TestParserPlot(unittest.TestCase):
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
