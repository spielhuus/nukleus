import sys
import unittest

from nukleus.model.HierarchicalSheetPin import HierarchicalSheetPin
from nukleus.SexpParser import load_tree

sys.path.append('src')
sys.path.append('..')

HIERARCHICAL_SHEET_PIN = """    (pin "VPP-MCLR" input (at 233.68 88.9 180)
      (effects (font (size 1.524 1.524)) (justify left))
      (uuid 4f5ccd8c-8f94-4906-8b6b-52cfd5ec3797)
    )"""

class TestHierarchicalSheetPin(unittest.TestCase):

    def test_parse_sheet_instance(self):
        sexp_str = load_tree(HIERARCHICAL_SHEET_PIN)
        pin = HierarchicalSheetPin.parse(sexp_str)
        self.assertEqual("VPP-MCLR", pin.name)
        self.assertEqual("input", pin.pin_type)

    def test_sexp_sheet_instance(self):
        sexp_str = load_tree(HIERARCHICAL_SHEET_PIN)
        sheet_instance = HierarchicalSheetPin.parse(sexp_str)
        self.assertEqual(HIERARCHICAL_SHEET_PIN, sheet_instance.sexp(indent=2))
