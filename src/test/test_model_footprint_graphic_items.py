
import sys
import unittest

sys.path.append('src')
sys.path.append('..')

from nukleus.model.FootprintGraphicsItems import FootprintLine
from nukleus.model.FootprintGraphicsItems import FootprintText
from nukleus.SexpParser import load_tree

INPUT_STRING_FPLINE = """    (fp_line (start 3.38 3.37) (end 5.18 3.37) (layer "F.SilkS") (width 0.12) (tstamp 3462ecc2-1bae-4a89-9f65-63a9e667d09c))"""
INPUT_STRING_TEXT = """     (fp_text value "100µF" (at 12.5 4.31 180) (layer "F.Fab")
      (effects (font (size 1 1) (thickness 0.15)))
      (tstamp 6714d3d0-67c3-4e88-bf4d-4c5f778e0892)
    )"""


class TestFootprintGraphicItem(unittest.TestCase):

    def test_parse_fpline(self):
        sexp_str = load_tree(INPUT_STRING_FPLINE)
        footprint = FootprintLine.parse(sexp_str)
        self.assertEqual((3.38, 3.37), footprint.start)
        self.assertEqual((5.18, 3.37), footprint.end)
        self.assertEqual("F.SilkS", footprint.layer)
        self.assertEqual(0.12, footprint.width)

    def test_parse_fptext(self):
        sexp_str = load_tree(INPUT_STRING_TEXT)
        footprint = FootprintText.parse(sexp_str)
        self.assertEqual((12.5, 4.31), footprint.pos)
        self.assertEqual(180, footprint.angle)
        self.assertEqual("100µF", footprint.text)
        self.assertEqual("value", footprint.text_type)
        self.assertEqual("F.Fab", footprint.layer)

