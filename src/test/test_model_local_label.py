import sys
import unittest

from nukleus.model.LocalLabel import LocalLabel
from nukleus.model.TextEffects import Justify, TextEffects
from nukleus.SexpParser import load_tree

sys.path.append('src')
sys.path.append('..')


INPUT_STRINGG = """  (label "IN_1" (at 96.52 45.72 270)
    (effects (font (size 1.27 1.27)) (justify right bottom))
    (uuid d9c6d5d2-0b49-49ba-a970-cd2c32f74c54)
  )"""


class TestLabel(unittest.TestCase):

    def test_parse_local_label(self):
        sexp_str = load_tree(INPUT_STRINGG)
        local_label = LocalLabel.parse(sexp_str)
        self.assertEqual('IN_1', local_label.text)
        self.assertEqual((96.52, 45.72), local_label.pos)
        self.assertEqual(270, local_label.angle)
        self.assertEqual('d9c6d5d2-0b49-49ba-a970-cd2c32f74c54',
                         local_label.identifier)
        self.assertEqual(
            TextEffects(font_height=1.27, font_width=1.27,
                        hidden=False, justify=[Justify.RIGHT, Justify.BOTTOM]),
            local_label.text_effects)

    def test_new_local_label(self):
        local_label = LocalLabel(identifier='d9c6d5d2-0b49-49ba-a970-cd2c32f74c54',
                                 pos=(96.52, 45.72), angle=270,
                                 text='IN_1',
                                 text_effects=TextEffects(font_height=1.27, font_width=1.27,
                                                          hidden=False,
                                                          justify=[Justify.RIGHT, Justify.BOTTOM]))
        self.assertEqual('IN_1', local_label.text)
        self.assertEqual((96.52, 45.72), local_label.pos)
        self.assertEqual(270, local_label.angle)
        self.assertEqual('d9c6d5d2-0b49-49ba-a970-cd2c32f74c54',
                         local_label.identifier)
        self.assertEqual(
            TextEffects(font_height=1.27, font_width=1.27,
                        hidden=False, justify=[Justify.RIGHT, Justify.BOTTOM]),
            local_label.text_effects)

    def test_sexp_local_label(self):
        sexp_str = load_tree(INPUT_STRINGG)
        symbol_instance = LocalLabel.parse(sexp_str)
        self.assertEqual(INPUT_STRINGG, symbol_instance.sexp())
