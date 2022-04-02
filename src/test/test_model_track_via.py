import sys
import unittest

from nukleus.model.TrackVia import TrackVia
from nukleus.SexpParser import load_tree

sys.path.append('src')
sys.path.append('..')

INPUT_STRINGG = """  (via (at 69.088 112.776) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 23) (tstamp f220d6a7-3170-4e04-8de6-2df0c3962fe0))"""


class TestTrackVia(unittest.TestCase):
    def test_parse_track_via(self):
        sexp_str = load_tree(INPUT_STRINGG)
        segment = TrackVia.parse(sexp_str)

        self.assertEqual((69.088, 112.776), segment.at)
        self.assertEqual(0.8, segment.size)
        self.assertEqual(0.4, segment.drill)
        self.assertEqual(['F.Cu', 'B.Cu'], segment.layers)
        self.assertEqual(23, segment.net)
        self.assertEqual('f220d6a7-3170-4e04-8de6-2df0c3962fe0', segment.tstamp)

    def test_pcb_setup_sexp(self):
        sexp_str = load_tree(INPUT_STRINGG)
        layers = TrackVia.parse(sexp_str)
        self.maxDiff=None
        self.assertEqual(INPUT_STRINGG, layers.sexp(indent=1))
