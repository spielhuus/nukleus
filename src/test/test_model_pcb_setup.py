import sys
import unittest

from nukleus.model.PcbSetup import PcbSetup
from nukleus.SexpParser import load_tree

sys.path.append('src')
sys.path.append('..')

INPUT_STRINGG = """  (setup
    (pad_to_mask_clearance 0)
    (pcbplotparams
      (layerselection 0x00010fc_ffffffff)
      (disableapertmacros false)
      (usegerberextensions false)
      (usegerberattributes true)
      (usegerberadvancedattributes true)
      (creategerberjobfile true)
      (svguseinch false)
      (svgprecision 6)
      (excludeedgelayer true)
      (plotframeref false)
      (viasonmask false)
      (mode 1)
      (useauxorigin false)
      (hpglpennumber 1)
      (hpglpenspeed 20)
      (hpglpendiameter 15.000000)
      (dxfpolygonmode true)
      (dxfimperialunits true)
      (dxfusepcbnewfont true)
      (psnegative false)
      (psa4output false)
      (plotreference true)
      (plotvalue true)
      (plotinvisibletext false)
      (sketchpadsonfab false)
      (subtractmaskfromsilk false)
      (outputformat 1)
      (mirror false)
      (drillshape 1)
      (scaleselection 1)
      (outputdirectory "")
    )
  )"""


class TestPcbSetup(unittest.TestCase):
    def test_parse_pcb_setup(self):
        sexp_str = load_tree(INPUT_STRINGG)
        setup = PcbSetup.parse(sexp_str)

        self.assertEqual(28, len(setup.values))
        self.assertEqual('0.25', setup.values['last_trace_width'])
        self.assertEqual('FFFFFF7F', setup.values['visible_elements'])
        self.assertEqual(26, len(setup.pcb_params))
        self.assertEqual('0x010fc_ffffffff', setup.values['layerselection'])
        self.assertEqual('1', setup.values['scaleselection'])

    def test_pcb_setup_sexp(self):
        sexp_str = load_tree(INPUT_STRINGG)
        layers = PcbSetup.parse(sexp_str)
        self.maxDiff=None
        self.assertEqual(INPUT_STRINGG, layers.sexp(indent=1))
