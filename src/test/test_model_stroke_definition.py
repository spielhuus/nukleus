import sys
import unittest

sys.path.append('src')
sys.path.append('..')

from nukleus.model.rgb import rgb
from nukleus.model.StrokeDefinition import StrokeDefinition
from nukleus.SexpParser import load_tree


class TestStrokeDefinition(unittest.TestCase):

    def test_parse_stroke_instance(self):
        sexp_str = load_tree("""    (stroke (width 0) (type default) (color 0 0 0 0))""")
        stroke_definition = StrokeDefinition.parse(sexp_str)
        self.assertEqual(0, stroke_definition.width)
        self.assertEqual('default', stroke_definition.type)
        self.assertEqual(rgb(0, 0, 0, 0), stroke_definition.color)

    def test_new_stroke_instance(self):
        symbol_instance = StrokeDefinition(width=0, type='default', color=rgb(0, 0, 0, 0))
        self.assertEqual(0, symbol_instance.width)
        self.assertEqual('default', symbol_instance.type)
        self.assertEqual(rgb(0, 0, 0, 0), symbol_instance.color)

    def test_sexp_stroke_instance(self):
        sexp_str = load_tree("""    (stroke (width 0) (type default) (color 0 0 0 0))""")
        symbol_instance = StrokeDefinition.parse(sexp_str)
        self.assertEqual(
                """    (stroke (width 0) (type default) (color 0 0 0 0))""",
                symbol_instance.sexp(indent=2))
