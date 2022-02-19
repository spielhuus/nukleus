import sys
import unittest

from nukleus.model.Property import Property
from nukleus.model.TextEffects import Justify, TextEffects
from nukleus.SexpParser import load_tree

sys.path.append('src')
sys.path.append('..')


INPUT_STRINGG = """      (property "Value" "TL072" (id 1) (at 0 -5.08 0)
        (effects (font (size 1.27 1.27)) (justify left))
      )"""


class TestProperty(unittest.TestCase):

    def test_parse_property(self):
        sexp_str = load_tree(INPUT_STRINGG)
        property = Property.parse(sexp_str)
        self.assertEqual((0, -5.08), property.pos)
        self.assertEqual(0, property.angle)
        self.assertEqual('Value', property.key)
        self.assertEqual('TL072', property.value)
        self.assertEqual(1, property.id)
        self.assertEqual(
            TextEffects(font_height=1.27, font_width=1.27,
                        hidden=False, justify=[Justify.LEFT]),
            property.text_effects)

    def test_new_property(self):
        property = Property(pos=(0, -5.08), angle=0, id=1, key="Value", value="TL072",
                            text_effects=TextEffects(font_height=1.27, font_width=1.27,
                                                     justify=[Justify.LEFT], hidden=False))
        self.assertEqual((0, -5.08), property.pos)
        self.assertEqual(0, property.angle)
        self.assertEqual('Value', property.key)
        self.assertEqual('TL072', property.value)
        self.assertEqual(1, property.id)
        self.assertEqual(
            TextEffects(font_height=1.27, font_width=1.27,
                        hidden=False, justify=[Justify.LEFT]),
            property.text_effects)

    def test_sexp_property(self):
        sexp_str = load_tree(INPUT_STRINGG)
        symbol_instance = Property.parse(sexp_str)
        self.assertEqual(INPUT_STRINGG, symbol_instance.sexp(indent=3))
