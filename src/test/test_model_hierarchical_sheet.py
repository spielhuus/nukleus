import sys
import unittest
from typing import List

from nukleus.model.HierarchicalSheet import HierarchicalSheet
from nukleus.SexpParser import load_tree

sys.path.append('src')
sys.path.append('..')

HIERARCHICAL_SHEET = """  (sheet (at 233.68 78.74) (size 39.37 30.48)
    (stroke (width 0) (type solid) (color 0 0 0 0))
    (fill (color 0 0 0 0))
    (uuid 00000000-0000-0000-0000-00004804a5e2)
    (property "Sheet name" "pic_sockets" (id 0) (at 233.68 77.9775 0)
      (effects (font (size 1.524 1.524)) (justify left bottom))
    )
    (property "Sheet file" "pic_sockets.kicad_sch" (id 1) (at 233.68 109.8301 0)
      (effects (font (size 1.524 1.524)) (justify left top))
    )
    (pin "VPP-MCLR" input (at 233.68 88.9 180)
      (effects (font (size 1.524 1.524)) (justify left))
      (uuid 4f5ccd8c-8f94-4906-8b6b-52cfd5ec3797)
    )
    (pin "CLOCK-RB6" input (at 233.68 105.41 180)
      (effects (font (size 1.524 1.524)) (justify left))
      (uuid 18190584-a843-4c9e-a97e-f2621f0a8d04)
    )
    (pin "DATA-RB7" input (at 233.68 97.79 180)
      (effects (font (size 1.524 1.524)) (justify left))
      (uuid 17d31f7d-0761-4df1-b4b6-3a74a68e0776)
    )
    (pin "VCC_PIC" input (at 233.68 81.28 180)
      (effects (font (size 1.524 1.524)) (justify left))
      (uuid 586ecb9b-c34b-43af-a37d-b273f3aea560)
    )
  )"""

class TestHierarchicalSheet(unittest.TestCase):

    def test_parse_sheet_instance(self):
        sexp_str = load_tree(HIERARCHICAL_SHEET)
        sheet = HierarchicalSheet.parse(sexp_str)
        self.assertEqual((233.68, 78.74), sheet.pos)
        self.assertEqual((39.37, 30.48), sheet.size)
        self.assertEqual(2, len(sheet.properties))
        self.assertEqual(4, len(sheet.pins))

    def test_sexp_sheet_instance(self):
        sexp_str = load_tree(HIERARCHICAL_SHEET)
        sheet_instance = HierarchicalSheet.parse(sexp_str)
        self.maxDiff = None
        self.assertEqual(HIERARCHICAL_SHEET, sheet_instance.sexp(indent=1))
