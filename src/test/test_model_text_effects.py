import sys
import unittest

sys.path.append('src')
sys.path.append('..')

from nukleus.model.TextEffects import TextEffects, Justify
from nukleus.model.rgb import rgb
from nukleus.SexpParser import load_tree

INPUT_STRING1 = """  (effects (font (size 1.27 1.27)) (justify right bottom) hide)"""
INPUT_STRING2 = """  (effects (font (size 2.54 2.54) (thickness 0.508) bold italic) (justify left bottom))"""

class TestTextEffects(unittest.TestCase):

    def test_parse_text_effects(self):
        sexp_str = load_tree(INPUT_STRING1)
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
        sexp_str = load_tree(INPUT_STRING1)
        symbol_instance = TextEffects.parse(sexp_str)
        self.assertEqual(INPUT_STRING1, symbol_instance.sexp())
    
    def test_sexp_text_effects_thickness(self):
        sexp_str = load_tree(INPUT_STRING2)
        symbol_instance = TextEffects.parse(sexp_str)
        self.assertEqual(INPUT_STRING2, symbol_instance.sexp())
