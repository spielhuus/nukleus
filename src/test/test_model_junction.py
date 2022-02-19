import sys
import unittest

sys.path.append('src')
sys.path.append('..')

from nukleus.model.Junction import Junction
from nukleus.model.rgb import rgb
from nukleus.SexpParser import load_tree

INPUT_STRINGG = """  (junction (at 93.98 163.83) (diameter 0) (color 0 0 0 0)
    (uuid e3fc1e69-a11c-4c84-8952-fefb9372474e)
  )"""

class TestJunction(unittest.TestCase):

    def test_parse_junction(self):
        sexp_str = load_tree(INPUT_STRINGG)
        junction = Junction.parse(sexp_str)
        self.assertEqual(
            'e3fc1e69-a11c-4c84-8952-fefb9372474e', junction.identifier)
        self.assertEqual((93.98, 163.83), junction.pos)
        self.assertEqual(0, junction.angle)
        self.assertEqual(0, junction.diameter)
        self.assertEqual(rgb(0, 0, 0, 0), junction.color)

    def test_new_junction(self):
        junction = Junction(pos=(115.57, 78.74),
                    identifier='e3fc1e69-a11c-4c84-8952-fefb9372474e',
                    angle=0, diameter=0, color=rgb(0, 0, 0, 0))
        self.assertEqual(
            'e3fc1e69-a11c-4c84-8952-fefb9372474e', junction.identifier)
        self.assertEqual((115.57, 78.74), junction.pos)
        self.assertEqual(0, junction.angle)
        self.assertEqual(0, junction.diameter)
        self.assertEqual(rgb(0, 0, 0, 0), junction.color)

    def test_sexp_junction(self):
        sexp_str = load_tree(INPUT_STRINGG)
        symbol_instance = Junction.parse(sexp_str)
        self.assertEqual(INPUT_STRINGG, symbol_instance.sexp())
