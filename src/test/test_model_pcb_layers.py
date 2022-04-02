import sys
import unittest

from nukleus.model.Layers import Layers
from nukleus.SexpParser import load_tree

sys.path.append("src")
sys.path.append("..")


INPUT_STRINGG = """  (layers
    (0 F.Cu signal)
    (31 B.Cu signal)
    (32 B.Adhes user)
    (33 F.Adhes user)
    (34 B.Paste user)
    (35 F.Paste user)
    (36 B.SilkS user)
    (37 F.SilkS user)
    (38 B.Mask user)
    (39 F.Mask user)
    (40 Dwgs.User user)
    (41 Cmts.User user)
    (42 Eco1.User user)
    (43 Eco2.User user)
    (44 Edge.Cuts user)
    (45 Margin user)
    (46 B.CrtYd user)
    (47 F.CrtYd user)
    (48 B.Fab user)
    (49 F.Fab user)
  )"""


class TestLayers(unittest.TestCase):
    def test_parse_layers(self):
        sexp_str = load_tree(INPUT_STRINGG)
        general = Layers.parse(sexp_str)

        self.assertEqual(20, len(general.layers))
        self.assertEqual(0, general.layers[0].ordinal)
        self.assertEqual("F.Cu", general.layers[0].canonical_name)
        self.assertEqual("signal", general.layers[0].type)
        self.assertEqual("", general.layers[1].user_name)

    def test_layers_sexp(self):
        sexp_str = load_tree(INPUT_STRINGG)
        layers = Layers.parse(sexp_str)
        self.assertEqual(INPUT_STRINGG, layers.sexp(indent=1))
