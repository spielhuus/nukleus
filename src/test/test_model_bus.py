import sys
import unittest

sys.path.append('src')
sys.path.append('..')

from nukleus.model.rgb import rgb
from nukleus.model.Bus import Bus
from nukleus.model.StrokeDefinition import StrokeDefinition
from nukleus.SexpParser import load_tree


class TestBus(unittest.TestCase):

    def test_parse_bus(self):
        sexp_str = load_tree("""  (bus (pts (xy 327.66 111.76) (xy 351.79 111.76))
    (stroke (width 0) (type solid) (color 0 0 0 0))
    (uuid 0c753b9e-5f93-4479-b1a6-b98503e7ca25)
  )""")
        bus = Bus.parse(sexp_str)
        self.assertEqual('0c753b9e-5f93-4479-b1a6-b98503e7ca25', bus.identifier)
        self.assertEqual([(327.66, 111.76), (351.79, 111.76)], bus.pts)
        self.assertEqual(StrokeDefinition(
            width=0, stroke_type='solid', color=rgb(0, 0, 0, 0)), bus.stroke_definition)

    def test_new_bus(self):
        bus = Bus(pts=[(327.66, 111.76), (351.79, 111.76)], 
                              identifier='0c753b9e-5f93-4479-b1a6-b98503e7ca25',
                              stroke_definition=StrokeDefinition(width=0, stroke_type='solid',
                                                                 color=rgb(0, 0, 0, 0)))
        self.assertEqual('0c753b9e-5f93-4479-b1a6-b98503e7ca25', bus.identifier)
        self.assertEqual([(327.66, 111.76), (351.79, 111.76)], bus.pts)
        self.assertEqual(StrokeDefinition(
            width=0, stroke_type='solid', color=rgb(0, 0, 0, 0)), bus.stroke_definition)

    def test_sexp_bus(self):
        sexp_str = load_tree("""  (bus (pts (xy 327.66 111.76) (xy 351.79 111.76))
    (stroke (width 0) (type solid) (color 0 0 0 0))
    (uuid 0c753b9e-5f93-4479-b1a6-b98503e7ca25)
  )""")
        symbol_instance = Bus.parse(sexp_str)
        self.assertEqual("""  (bus (pts (xy 327.66 111.76) (xy 351.79 111.76))
    (stroke (width 0) (type solid) (color 0 0 0 0))
    (uuid 0c753b9e-5f93-4479-b1a6-b98503e7ca25)
  )""", symbol_instance.sexp())
