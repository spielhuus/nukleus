import sys
import unittest

sys.path.append('src')
sys.path.append('..')

from nukleus.model.TextEffects import TextEffects, Justify
from nukleus.model.rgb import rgb
from nukleus.SexpParser import load_tree

INPUT_STRINGG = """  (effects (font (size 1.27 1.27)) (justify right bottom) hide)"""

class TestTextEffects(unittest.TestCase):

    def test_parse_text_effects(self):
        sexp_str = load_tree(INPUT_STRINGG)
        text_effects = TextEffects.parse(sexp_str)
        self.assertEqual(1.27, text_effects.font_width)
        self.assertEqual(1.27, text_effects.font_height)
        self.assertEqual('', text_effects.font_thickness)
        self.assertEqual('', text_effects.font_style)
        self.assertEqual([Justify.RIGHT, Justify.BOTTOM], text_effects.justify)
        self.assertEqual(True, text_effects.hidden)

    def test_new_text_effects(self):
        text_effects = TextEffects(font_height=1.27, font_width=1.27, font_thickness='',
                                   font_style='', justify=[Justify.RIGHT, Justify.BOTTOM],
                                   hidden=True)
        self.assertEqual(1.27, text_effects.font_width)
        self.assertEqual(1.27, text_effects.font_height)
        self.assertEqual('', text_effects.font_thickness)
        self.assertEqual('', text_effects.font_style)
        self.assertEqual([Justify.RIGHT, Justify.BOTTOM], text_effects.justify)
        self.assertEqual(True, text_effects.hidden)

    def test_sexp_text_effects(self):
        sexp_str = load_tree(INPUT_STRINGG)
        symbol_instance = TextEffects.parse(sexp_str)
        self.assertEqual(INPUT_STRINGG, symbol_instance.sexp())
