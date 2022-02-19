import sys
import unittest

from nukleus.model.LibrarySymbol import LibrarySymbol
from nukleus.model.TextEffects import Justify, TextEffects
from nukleus.SexpParser import load_tree

sys.path.append('src')
sys.path.append('..')


INPUT_STRINGG = """    (symbol "Device:R" (pin_numbers hide) (pin_names (offset 0)) (in_bom yes) (on_board yes)
      (property "Reference" "R" (id 0) (at 2.032 0 90)
        (effects (font (size 1.27 1.27)))
      )
      (property "Value" "R" (id 1) (at 0 0 90)
        (effects (font (size 1.27 1.27)))
      )
      (property "Footprint" "" (id 2) (at -1.778 0 90)
        (effects (font (size 1.27 1.27)) hide)
      )
      (property "Datasheet" "~" (id 3) (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (property "ki_keywords" "R res resistor" (id 4) (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (property "ki_description" "Resistor" (id 5) (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (property "ki_fp_filters" "R_*" (id 6) (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (symbol "R_0_1"
        (rectangle (start -1.016 -2.54) (end 1.016 2.54)
          (stroke (width 0.254) (type default) (color 0 0 0 0))
          (fill (type none))
        )
      )
      (symbol "R_1_1"
        (pin passive line (at 0 3.81 270) (length 1.27)
          (name "~" (effects (font (size 1.27 1.27))))
          (number "1" (effects (font (size 1.27 1.27))))
        )
        (pin passive line (at 0 -3.81 90) (length 1.27)
          (name "~" (effects (font (size 1.27 1.27))))
          (number "2" (effects (font (size 1.27 1.27))))
        )
      )
    )"""


class TestProperty(unittest.TestCase):

#    def test_parse_property(self):
#        sexp_str = load_tree(INPUT_STRINGG)
#        property = Property.parse(sexp_str)
#        self.assertEqual((0, -5.08), property.pos)
#        self.assertEqual(0, property.angle)
#        self.assertEqual('Value', property.key)
#        self.assertEqual('TL072', property.value)
#        self.assertEqual(1, property.id)
#        self.assertEqual(
#            TextEffects(font_height=1.27, font_width=1.27,
#                        hidden=False, justify=[Justify.LEFT]),
#            property.text_effects)
#
#    def test_new_property(self):
#        property = Property(pos=(0, -5.08), angle=0, id=1, key="Value", value="TL072",
#                            text_effects=TextEffects(font_height=1.27, font_width=1.27,
#                                                     justify=[Justify.LEFT], hidden=False))
#        self.assertEqual((0, -5.08), property.pos)
#        self.assertEqual(0, property.angle)
#        self.assertEqual('Value', property.key)
#        self.assertEqual('TL072', property.value)
#        self.assertEqual(1, property.id)
#        self.assertEqual(
#            TextEffects(font_height=1.27, font_width=1.27,
#                        hidden=False, justify=[Justify.LEFT]),
#            property.text_effects)

    def test_sexp_library_symbol(self):
        sexp_str = load_tree(INPUT_STRINGG)
        symbol_instance = LibrarySymbol.parse(sexp_str)
        self.assertEqual(INPUT_STRINGG, symbol_instance.sexp(indent=2))
