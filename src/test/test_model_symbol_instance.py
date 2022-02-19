from typing import List
import unittest

import sys
sys.path.append('src')
sys.path.append('..')

from nukleus.SexpParser import load_tree
from nukleus.model.SymbolInstanceSection import  SymbolInstanceSection

class TestSymbolInstanceSection(unittest.TestCase):
    
    def test_parse_symbol_instance(self):
        sexp_str = load_tree("""    (path "/00000000-0000-0000-0000-000061bc0ef5"
      (reference "C1") (unit 1) (value "0.1u") (footprint "Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder")
    )""")
        symbol_instance = SymbolInstanceSection.parse(sexp_str)
        self.assertEqual("/00000000-0000-0000-0000-000061bc0ef5", symbol_instance.path)
        self.assertEqual("C1", symbol_instance.reference)
        self.assertEqual(1, symbol_instance.unit)
        self.assertEqual("0.1u", symbol_instance.value)
        self.assertEqual("Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder",
                         symbol_instance.footprint)

    def test_new_symbol_instance(self):
        symbol_instance = SymbolInstanceSection(
                path="/00000000-0000-0000-0000-000061bc0ef5",
                reference="C1", unit=1, value="0.1u",
                footprint="Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder")
        self.assertEqual("/00000000-0000-0000-0000-000061bc0ef5", symbol_instance.path)
        self.assertEqual("C1", symbol_instance.reference)
        self.assertEqual(1, symbol_instance.unit)
        self.assertEqual("0.1u", symbol_instance.value)
        self.assertEqual("Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder",
                         symbol_instance.footprint)

    def test_sexp_symbol_instance(self):
        sexp_str = load_tree("""    (path "/00000000-0000-0000-0000-000061bc0ef5"
      (reference "C1") (unit 1) (value "0.1u") (footprint "Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder")
    )""")
        symbol_instance = SymbolInstanceSection.parse(sexp_str)
        self.assertEqual("""    (path "/00000000-0000-0000-0000-000061bc0ef5"
      (reference "C1") (unit 1) (value "0.1u") (footprint "Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder")
    )""", symbol_instance.sexp(indent=2))
