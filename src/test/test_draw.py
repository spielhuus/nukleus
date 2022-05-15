import sys
import unittest

sys.path.append("src")

from nukleus.SexpParser import load_tree
from nukleus.ParserVisitor import ParserVisitor
from nukleus.SchemaDraw import SchemaDraw
from nukleus.draw.Line import Line
from nukleus.ModelSchema import Wire

class TestDraw(unittest.TestCase):
    def test_draw(self):
        draw = SchemaDraw()
        draw.add(Line())

        self.assertEqual(1, len(draw.content[Wire]))
