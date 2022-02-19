import sys
import unittest

from nukleus.model.Pin import Pin
from nukleus.model.TextEffects import TextEffects
from nukleus.SexpParser import load_tree

sys.path.append('src')
sys.path.append('..')


INPUT_STRINGG = """        (pin output line (at 7.62 0 180) (length 2.54)
          (name "~" (effects (font (size 1.27 1.27))))
          (number "1" (effects (font (size 1.27 1.27))))
        )"""


class TestPin(unittest.TestCase):

    def test_parse_pin(self):
        sexp_str = load_tree(INPUT_STRINGG)
        pin = Pin.parse(sexp_str)
        self.assertEqual((7.62, 0), pin.pos)
        self.assertEqual(180, pin.angle)
        self.assertEqual('output', pin.type)
        self.assertEqual('line', pin.style)
        self.assertEqual(2.54, pin.length)
        self.assertEqual(
            ('~', TextEffects(font_height=1.27, font_width=1.27, hidden=False)), pin.name)
        self.assertEqual(
            ('1', TextEffects(font_height=1.27, font_width=1.27, hidden=False)), pin.number)

    def test_new_pin(self):
        pin = Pin(pos=(7.62, 0), angle=180, length=2.54,
                  name=('~', TextEffects(font_height=1.27, font_width=1.27)),
                  number=('1', TextEffects(font_height=1.27, font_width=1.27)))
        self.assertEqual((7.62, 0), pin.pos)
        self.assertEqual(180, pin.angle)
        self.assertEqual(2.54, pin.length)
        self.assertEqual(
            ('~', TextEffects(font_height=1.27, font_width=1.27)), pin.name)
        self.assertEqual(
            ('1', TextEffects(font_height=1.27, font_width=1.27)), pin.number)

    def test_sexp_pin(self):
        sexp_str = load_tree(INPUT_STRINGG)
        symbol_instance = Pin.parse(sexp_str)
        self.assertEqual(INPUT_STRINGG, symbol_instance.sexp(indent=4))
