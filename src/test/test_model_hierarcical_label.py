import sys
import unittest
from typing import List

from nukleus.model.HierarchicalLabel import HierarchicalLabel, HierarchicalLabelShape
from nukleus.SexpParser import load_tree

sys.path.append('src')
sys.path.append('..')

HIERARCHICAL_LABEL = """  (hierarchical_label "RAS6-" (shape input) (at 212.09 181.61 180)
    (effects (font (size 1.524 1.524)) (justify right))
    (uuid 2370ec94-b3a1-4a98-8c0a-a183cc2fa704)
  )"""

class TestHierarchicalLabel(unittest.TestCase):

    def test_parse_hierarchical_label(self):
        sexp_str = load_tree(HIERARCHICAL_LABEL)
        sheet = HierarchicalLabel.parse(sexp_str)
        self.assertEqual((212.09, 181.61), sheet.pos)
        self.assertEqual(180, sheet.angle)
        self.assertEqual(HierarchicalLabelShape.INPUT, sheet.shape)

    def test_sexp_hierarchical_label(self):
        sexp_str = load_tree(HIERARCHICAL_LABEL)
        sheet_instance = HierarchicalLabel.parse(sexp_str)
        self.maxDiff = None
        self.assertEqual(HIERARCHICAL_LABEL, sheet_instance.sexp(indent=1))
