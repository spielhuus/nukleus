import sys
import unittest
from typing import List

from nukleus.model.HierarchicalSheetInstance import HierarchicalSheetInstance
from nukleus.SexpParser import load_tree

sys.path.append('src')
sys.path.append('..')

class TestHierarchicalSheetInstance(unittest.TestCase):

    def test_parse_symbol_instance(self):
        sexp_str = load_tree("""    (path "/" (page "1"))""")
        sheet_instance = HierarchicalSheetInstance.parse(sexp_str)
        self.assertEqual("/", sheet_instance.path)
        self.assertEqual(1, sheet_instance.page)

    def test_new_symbol_instance(self):
        sheet_instance = HierarchicalSheetInstance(path="/", page=1)
        self.assertEqual("/", sheet_instance.path)
        self.assertEqual(1, sheet_instance.page)

    def test_sexp_symbol_instance(self):
        sexp_str = load_tree("""    (path "/" (page "1"))""")
        sheet_instance = HierarchicalSheetInstance.parse(sexp_str)
        self.assertEqual("""    (path "/" (page "1"))""", sheet_instance.sexp(indent=2))
