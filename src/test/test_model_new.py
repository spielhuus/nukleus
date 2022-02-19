import sys

from nukleus.model.StrokeDefinition import StrokeDefinition
from nukleus.model.TextEffects import Justify
sys.path.append('src')
sys.path.append('../../src')

import unittest
from unittest.mock import MagicMock, patch
import re
import uuid

from sys import path
path.append('src')

from nukleus.model import BusEntry, Bus, HierarchicalLabel, LocalLabel, GlobalLabel, \
                          GraphicalLine, GraphicalText, HierarchicalLabel, Symbol, \
                          Pin, PinList, Property, Wire, HierarchicalSheet

uuid4hex = re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', re.I)

_uuid = '770ad51a-7219-4633-b24a-bd20feb0a6c5'
def mock_uuid():
    return uuid.UUID(_uuid)


#@patch('uuid.uuid4', side_effect=mock_uuid)
#class TestModelNew(unittest.TestCase):
#    def test_new_bus_entry(self, _):
#        bus = BusEntry.new()
#        self.assertTrue(isinstance(bus, BusEntry))
#        self.assertTrue(uuid4hex.match(bus.identifier))
#        self.assertEqual((0, 0), bus.pos)
#        self.assertEqual(0, bus.angle)
#        self.assertEqual(f"""  (bus_entry (at 0 0) (size 0 0)
#    (stroke (width 0) (type solid) (color 0 0 0 0))
#    (uuid {_uuid})
#  )""", bus.sexp())
#
##    def test_new_bus(self, _):
##        bus = Bus.new()
##        self.assertTrue(isinstance(bus, Bus))
##        self.assertTrue(uuid4hex.match(bus.identifier))
##        self.assertEqual([(0, 0), (0, 0)], bus.pts)
##        self.assertTrue(isinstance(bus.stroke_definition, StrokeDefinition))
##        self.assertEqual("""  (bus (pts (xy 0 0) (xy 0 0))
##    (stroke (width 0) (type solid) (color 0 0 0 0))
##    (uuid 770ad51a-7219-4633-b24a-bd20feb0a6c5)
##  )""", bus.sexp())
#
#    def test_new_global_label(self, mock):
#        glabel = GlobalLabel.new()
#        glabel.text_effects.justify.append(Justify.LEFT)
#        glabel.properties.append(Property.new('Intersheet References', '${INTERSHEET_REFS}'))
#        self.assertTrue(isinstance(glabel, GlobalLabel))
#        self.assertTrue(uuid4hex.match(glabel.identifier))
#        self.assertEqual((0, 0), glabel.pos)
#        self.assertEqual(0, glabel.angle)
#        self.assertEqual('', glabel.text, StrokeDefinition)
#        self.maxDiff = None
#        self.assertEqual(f"""  (global_label "" (shape output) (at 0 0 0)
#    (effects (font (size 0 0)) (justify left))
#    (uuid {_uuid})
#    (property "Intersheet References" "${{INTERSHEET_REFS}}" (id 1) (at 0 0 0)
#      (effects (font (size 0 0)) hide)
#    )
#  )""", glabel.sexp())
#
#    def test_new_local_label(self, mock):
#        label = LocalLabel.new()
#        label.text_effects.justify.append(Justify.LEFT)
#        label.text_effects.justify.append(Justify.BOTTOM)
#        self.assertTrue(isinstance(label, LocalLabel))
#        self.assertTrue(uuid4hex.match(label.identifier))
#        self.assertEqual((0, 0), label.pos)
#        self.assertEqual(0, label.angle)
#        self.assertEqual('', label.text, StrokeDefinition)
#        self.assertEqual("""  (label "" (at 0 0 0)
#    (effects (font (size 0 0)) (justify left bottom))
#    (uuid 770ad51a-7219-4633-b24a-bd20feb0a6c5)
#  )""", label.sexp())
#
#    def test_new_graphical_line(self, mock):
#        gline = GraphicalLine.new()
#        self.assertTrue(isinstance(gline, GraphicalLine))
#        self.assertTrue(uuid4hex.match(gline.identifier))
#        self.assertEqual([(0, 0), (0, 0)], gline.pts)
#        self.assertEqual(f"""  (polyline (pts (xy 0 0) (xy 0 0))
#    (stroke (width 0) (type solid) (color 0 0 0 0))
#    (uuid {_uuid})
#  )""", gline.sexp())
#
##    def test_new_graphical_text(self, mock):
##        gtext = GraphicalText.new()
##        self.assertTrue(isinstance(gtext, GraphicalText))
##        self.assertTrue(uuid4hex.match(gtext.identifier))
##        self.assertEqual([(0, 0), (0, 0)], gtext.pts)
##
##        self.assertEqual("""  (text "TXD" (at 46.99 91.44 0)
##    (effects (font (size 1.524 1.524)) (justify left bottom))
##    (uuid 1a3d63d6-4cc1-44e5-89c4-24c18535d780)
##   )""", gtext.sexp())
#
##    def test_new_graphic_item(self, mock):
##        gtext = GraphicItem.new()
##        self.assertTrue(isinstance(gtext, GraphicalText))
##        self.assertTrue(uuid4hex.match(gtext.identifier))
##        self.assertEqual([(0, 0), (0, 0)], gtext.pts)
##
##        self.assertEqual("""  (text "TXD" (at 46.99 91.44 0)
##    (effects (font (size 1.524 1.524)) (justify left bottom))
##    (uuid 1a3d63d6-4cc1-44e5-89c4-24c18535d780)
##   )""", gtext.sexp())
#
#    def test_new_hierarchical_label(self, mock):
#        hlabel = HierarchicalLabel.new()
#        hlabel.text_effects.justify.append(Justify.LEFT)
#        self.assertTrue(isinstance(hlabel, HierarchicalLabel))
#        self.assertTrue(uuid4hex.match(hlabel.identifier))
#        self.assertEqual((0, 0), hlabel.pos)
#        self.assertEqual(f"""  (hierarchical_label "" (shape bidirectional) (at 0 0)
#    (effects (font (size 0 0)) (justify left))
#    (uuid {_uuid})
#  )""", hlabel.sexp())
#
##    def test_new_hierarchical_sheet(self, mock):
##        sheet = HierarchicalSheet.new()
##        self.assertTrue(isinstance(sheet, HierarchicalSheet))
##        self.assertTrue(uuid4hex.match(sheet.identifier))
##        self.assertEqual((0, 0), sheet.pos)
##        print(f"\n{sheet.sexp()}")
##        self.assertEqual(f"""  (sheet (at 0 0) (size 0 0)
##    (stroke (width 0) (type solid) (color 0 0 0 0)))
##    (fill (color 0 0 0 0))
##    (uuid {_uuid})
##    (property "Sheet name" "" (id 1) (at 0 0 0)
##      (effects (font (size 0 0) hide))
##    )
##    (property "Sheet file" "" (id 1) (at 0 0 0)
##      (effects (font (size 1.524 1.524) hide)
##    )
##  )""", sheet.sexp())
#
#    def test_new_wire(self, mock):
#        wire = Wire.new()
#        self.assertTrue(isinstance(wire, Wire))
#        self.assertTrue(uuid4hex.match(wire.identifier))
#        self.assertEqual([(0, 0), (0, 0)], wire.pts)
#        self.assertEqual("""  (wire (pts (xy 0 0) (xy 0 0))
#    (stroke (width 0) (type solid) (color 0 0 0 0))
#    (uuid 770ad51a-7219-4633-b24a-bd20feb0a6c5)
#  )""", wire.sexp())
