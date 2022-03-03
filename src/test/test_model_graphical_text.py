import sys
import unittest

sys.path.append('src')
sys.path.append('..')

from nukleus.model.GraphicalText import GraphicalText
from nukleus.SexpParser import load_tree


class TestGraphicalLine(unittest.TestCase):

    def test_parse_graphical_text(self):
        sexp_str = load_tree(
                """    (text "resistor R25 must be connected to inverting input" (at 38.1 127 0)
    (effects (font (size 1.27 1.27)) (justify left bottom))
    (uuid 22bb6c80-05a9-4d89-98b0-f4c23fe6c1ce)
  )""")
        graphical_text = GraphicalText.parse(sexp_str)
        self.assertEqual(
            '22bb6c80-05a9-4d89-98b0-f4c23fe6c1ce', graphical_text.identifier)
        self.assertEqual((38.1, 127), graphical_text.pos)
        self.assertEqual(0, graphical_text.angle)
        self.assertEqual('resistor R25 must be connected to inverting input', graphical_text.text)

    def test_new_graphical_text(self):
        graphical_text = GraphicalText(pos=(115.57, 78.74),
                    identifier='eae0ab9f-65b2-44d3-aba7-873c3227fba7',
                    angle=0,
                    text='resistor R25 must be connected to inverting input')
        self.assertEqual(
            'eae0ab9f-65b2-44d3-aba7-873c3227fba7', graphical_text.identifier)
        self.assertEqual((115.57, 78.74), graphical_text.pos)
        self.assertEqual(0, graphical_text.angle)
        self.assertEqual('resistor R25 must be connected to inverting input', graphical_text.text)

    def test_sexp_graphical_text(self):
        sexp_str = load_tree("""    (text "resistor R25 must be connected to inverting input" (at 38.1 127 0)
    (effects (font (size 1.27 1.27)) (justify left bottom))
    (uuid 22bb6c80-05a9-4d89-98b0-f4c23fe6c1ce)
  )""")
        symbol_instance = GraphicalText.parse(sexp_str)
        self.maxDiff = None
        self.assertEqual("""  (text "resistor R25 must be connected to inverting input" (at 38.1 127 0)
    (effects (font (size 1.27 1.27)) (justify left bottom))
    (uuid 22bb6c80-05a9-4d89-98b0-f4c23fe6c1ce)
  )""", symbol_instance.sexp())
