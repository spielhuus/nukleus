import sys
import unittest

from nukleus.model.GraphicalLine import GraphicalLine
from nukleus.SexpParser import load_tree

sys.path.append('src')
sys.path.append('..')

GRAPHICAL_LINE = """  (polyline (pts (xy 172.72 170.18) (xy 172.72 196.85))
    (stroke (width 0) (type dash) (color 0 0 0 0))
    (uuid 12d34910-9c6c-4880-b730-cafdbf5d87ee)
  )"""

class TestGraphicalLine(unittest.TestCase):

    def test_parse_graphical_line(self):
        sexp_str = load_tree(GRAPHICAL_LINE)
        sheet = GraphicalLine.parse(sexp_str)
        self.assertEqual([(172.72, 170.18), (172.72, 196.85)], sheet.pts)

    def test_sexp_graphical_line(self):
        sexp_str = load_tree(GRAPHICAL_LINE)
        sheet_instance = GraphicalLine.parse(sexp_str)
        self.maxDiff = None
        self.assertEqual(GRAPHICAL_LINE, sheet_instance.sexp(indent=1))
