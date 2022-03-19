import sys
import unittest

sys.path.append('src')
sys.path.append('..')

from nukleus.model.rgb import rgb
from nukleus.model.BusEntry import BusEntry
from nukleus.model.StrokeDefinition import StrokeDefinition
from nukleus.SexpParser import load_tree


class TestBus(unittest.TestCase):

    def test_parse_bus(self):
        sexp_str = load_tree("""  (bus_entry (at 140.97 161.29) (size 2.54 -2.54)
    (stroke (width 0.1524) (type solid) (color 0 0 0 0))
    (uuid ca2cc51e-1efa-48be-969c-d8fb55c8b635)
  )""")
        bus = BusEntry.parse(sexp_str)
        self.assertEqual('ca2cc51e-1efa-48be-969c-d8fb55c8b635', bus.identifier)
        self.assertEqual((140.97, 161.29), bus.pos)
        self.assertEqual((2.54, -2.54), bus.size)
        self.assertEqual(StrokeDefinition(
            width=0.1524, stroke_type='solid', color=rgb(0, 0, 0, 0)), bus.stroke_definition)

    def test_sexp_bus(self):
        sexp_str = load_tree("""  (bus_entry (at 140.97 161.29) (size 2.54 -2.54)
    (stroke (width 0.1524) (type solid) (color 0 0 0 0))
    (uuid ca2cc51e-1efa-48be-969c-d8fb55c8b635)
  )""")
        symbol_instance = BusEntry.parse(sexp_str)
        self.assertEqual("""  (bus_entry (at 140.97 161.29) (size 2.54 -2.54)
    (stroke (width 0.1524) (type solid) (color 0 0 0 0))
    (uuid ca2cc51e-1efa-48be-969c-d8fb55c8b635)
  )""", symbol_instance.sexp())
