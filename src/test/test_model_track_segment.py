import sys
import unittest

from nukleus.model.TrackSegment import TrackSegment
from nukleus.SexpParser import load_tree

sys.path.append('src')
sys.path.append('..')

INPUT_STRINGG = """  (segment (start 61.976 103.124) (end 62.775999 103.923999) (width 0.381) (layer "F.Cu") (net 1) (tstamp 9208ea78-8dde-4b3d-91e9-5755ab5efd9a))"""


class TestTrackSegment(unittest.TestCase):
    def test_parse_track_via(self):
        sexp_str = load_tree(INPUT_STRINGG)
        segment = TrackSegment.parse(sexp_str)

        self.assertEqual((61.976, 103.124), segment.start)
        self.assertEqual((62.775999, 103.923999), segment.end)
        self.assertEqual(0.381, segment.width)
        self.assertEqual('F.Cu', segment.layer)
        self.assertEqual(1, segment.net)
        self.assertEqual(False, segment.locked)
        self.assertEqual('9208ea78-8dde-4b3d-91e9-5755ab5efd9a', segment.tstamp)

    def test_pcb_setup_sexp(self):
        sexp_str = load_tree(INPUT_STRINGG)
        layers = TrackSegment.parse(sexp_str)
        self.maxDiff=None
        self.assertEqual(INPUT_STRINGG, layers.sexp(indent=1))
