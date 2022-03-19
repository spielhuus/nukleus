import sys
import unittest

sys.path.append('src')
sys.path.append('..')

from nukleus.model.rgb import rgb
from nukleus.model.StrokeDefinition import StrokeDefinition
from nukleus.model.Wire import Wire
from nukleus.SexpParser import load_tree


class Testwire(unittest.TestCase):

    def test_parse_wire(self):
        sexp_str = load_tree("""  (wire (pts (xy 87.63 156.21) (xy 87.63 158.75))
    (stroke (width 0) (type default) (color 0 0 0 0))
    (uuid 592f25e6-a01b-47fd-8172-3da01117d00a)
  )""")
        wire = Wire.parse(sexp_str)
        self.assertEqual(
            '592f25e6-a01b-47fd-8172-3da01117d00a', wire.identifier)
        self.assertEqual([(87.63, 156.21), (87.63, 158.75)], wire.pts)
        self.assertEqual(StrokeDefinition(
            width=0, stroke_type='default', color=rgb(0, 0, 0, 0)), wire.stroke_definition)

    def test_new_wire(self):
        wire = Wire(pts=[(87.63, 156.21), (87.63, 158.75)],
                    identifier='592f25e6-a01b-47fd-8172-3da01117d00a',
                    stroke_definition=StrokeDefinition(width=0, stroke_type='solid',
                                                       color=rgb(0, 0, 0, 0)))
        self.assertEqual(
            '592f25e6-a01b-47fd-8172-3da01117d00a', wire.identifier)
        self.assertEqual([(87.63, 156.21), (87.63, 158.75)], wire.pts)
        self.assertEqual(StrokeDefinition(
            width=0, stroke_type='solid', color=rgb(0, 0, 0, 0)), wire.stroke_definition)

    def test_sexp_wire(self):
        sexp_str = load_tree("""  (wire (pts (xy 87.63 156.21) (xy 87.63 158.75))
    (stroke (width 0) (type default) (color 0 0 0 0))
    (uuid 592f25e6-a01b-47fd-8172-3da01117d00a)
  )""")
        symbol_instance = Wire.parse(sexp_str)
        self.assertEqual("""  (wire (pts (xy 87.63 156.21) (xy 87.63 158.75))
    (stroke (width 0) (type default) (color 0 0 0 0))
    (uuid 592f25e6-a01b-47fd-8172-3da01117d00a)
  )""", symbol_instance.sexp())
