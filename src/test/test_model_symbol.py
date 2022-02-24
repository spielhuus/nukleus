import sys
import unittest

sys.path.append("src")
sys.path.append("..")

from nukleus.Library import Library
from nukleus.model.rgb import rgb
from nukleus.model.Symbol import Symbol
from nukleus.SexpParser import load_tree

INPUT_STRINGG = """  (symbol (lib_id "Device:R") (at 88.9 33.02 270) (unit 1)
    (in_bom yes) (on_board yes)
    (uuid 00000000-0000-0000-0000-00005ea43020)
    (property "Reference" "R4" (id 0) (at 88.9 27.7622 90))
    (property "Value" "100k" (id 1) (at 88.9 30.0736 90))
    (property "Footprint" "Resistor_SMD:R_0805_2012Metric_Pad1.20x1.40mm_HandSolder" (id 2) (at 88.9 31.242 90)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" "~" (id 3) (at 88.9 33.02 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Description" "Thick Film Resistors - SMD (0805)" (id 4) (at 88.9 33.02 90)
      (effects (font (size 1.27 1.27)) hide)
    )
    (pin "1" (uuid 7f41b6ad-3624-48a6-a0d2-d278e9f52b3d))
    (pin "2" (uuid 5f4fd338-1c9e-4638-abf9-b24cce2a1173))
  )"""


class TestSymbol(unittest.TestCase):
    def test_parse_symbol(self):
        sexp_str = load_tree(INPUT_STRINGG)
        symbol = Symbol.parse(sexp_str)

    def test_new_resistor(self):
        lib = Library(["samples/files/symbols"])
        lib_sym = lib.get("Device:R")
        self.assertEqual("R", lib_sym.identifier)
        self.assertEqual(2, len(lib_sym.units))

        symbol = Symbol.new('R1', 'Device:R', lib_sym, unit=1)
        #TODO write test TestCase

    def test_new_opamp(self):
        lib = Library(["samples/files/symbols"])
        lib_sym = lib.get("Amplifier_Operational:TL072")
        self.assertEqual("TL072", lib_sym.identifier)
        self.assertEqual(3, len(lib_sym.units))
        
        symbol = Symbol.new('U1', 'Amplifier_Operational:TL072', lib_sym, unit=1)
        #TODO write test TestCase

    def test_new_opamp_power(self):
        lib = Library(["samples/files/symbols"])
        lib_sym = lib.get("Amplifier_Operational:TL072")
        self.assertEqual("TL072", lib_sym.identifier)
        self.assertEqual(3, len(lib_sym.units))
        
        symbol = Symbol.new('U1', 'Amplifier_Operational:TL072', lib_sym, unit=3)
        #TODO write test TestCase
    def test_sexp_symbol(self):
        sexp_str = load_tree(INPUT_STRINGG)
        symbol_instance = Symbol.parse(sexp_str)
        self.assertEqual(INPUT_STRINGG, symbol_instance.sexp())
