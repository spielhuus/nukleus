import sys
import unittest

sys.path.append('src')
sys.path.append('..')

from nukleus.model.PcbSetup import PcbSetup
from nukleus.SexpParser import load_tree


INPUT_STRINGG = """  (setup
    (stackup
      (layer "F.SilkS" (type "Top Silk Screen") (color "White"))
      (layer "F.Paste" (type "Top Solder Paste"))
      (layer "F.Mask" (type "Top Solder Mask") (color "Green") (thickness 0.01))
      (layer "F.Cu" (type "copper") (thickness 0.035))
      (layer "dielectric 1" (type "core") (thickness 0.480066) (material "FR4") (epsilon_r 4.5) (loss_tangent 0.02))
      (layer "In1.Cu" (type "copper") (thickness 0.035))
      (layer "dielectric 2" (type "prepreg") (thickness 0.480066) (material "FR4") (epsilon_r 4.5) (loss_tangent 0.02))
      (layer "In2.Cu" (type "copper") (thickness 0.035))
      (layer "dielectric 3" (type "core") (thickness 0.480066) (material "FR4") (epsilon_r 4.5) (loss_tangent 0.02))
      (layer "B.Cu" (type "copper") (thickness 0.035))
      (layer "B.Mask" (type "Bottom Solder Mask") (color "Green") (thickness 0.01))
      (layer "B.Paste" (type "Bottom Solder Paste"))
      (layer "B.SilkS" (type "Bottom Silk Screen") (color "White"))
      (copper_finish "HAL lead-free")
      (dielectric_constraints no)
    )
    (pad_to_mask_clearance 0)
    (aux_axis_origin 40.9 173.1)
    (pcbplotparams
      (layerselection 0x00010fc_ffffffff)
      (disableapertmacros false)
      (usegerberextensions false)
      (usegerberattributes true)
      (usegerberadvancedattributes true)
      (creategerberjobfile true)
      (svguseinch false)
      (svgprecision 6)
      (excludeedgelayer false)
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
      (drillshape 0)
      (scaleselection 1)
      (outputdirectory "plots")
    )
  )"""


class TestPcbSetup(unittest.TestCase):
    def test_parse_pcb_setup(self):
        sexp_str = load_tree(INPUT_STRINGG)
        setup = PcbSetup.parse(sexp_str)

        self.assertEqual('0', setup.pad_to_mask_clearance)
        self.assertEqual([40.9, 173.1], setup.aux_axis_origin)
        self.assertEqual(13, len(setup.stackup_settings.layers))
        self.assertEqual("dielectric 1", setup.stackup_settings.layers[4].name)
        self.assertEqual("core", setup.stackup_settings.layers[4].type)
        self.assertEqual(0.480066, setup.stackup_settings.layers[4].thickness)
        self.assertEqual("FR4", setup.stackup_settings.layers[4].material)
        self.assertEqual(4.5, setup.stackup_settings.layers[4].epsilon_r)
        self.assertEqual(0.02, setup.stackup_settings.layers[4].loss_tangent)
        self.assertEqual('HAL lead-free', setup.stackup_settings.copper_finish)
        self.assertEqual('no', setup.stackup_settings.dielectric_constraints)
        self.assertEqual('0x00010fc_ffffffff', setup.plot_settings.layerselection)

    def test_pcb_setup_sexp(self):
        sexp_str = load_tree(INPUT_STRINGG)
        layers = PcbSetup.parse(sexp_str)
        self.maxDiff=None
        self.assertEqual(INPUT_STRINGG, layers.sexp(indent=1))
