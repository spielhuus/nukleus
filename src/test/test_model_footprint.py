import sys
import unittest

sys.path.append('src')
sys.path.append('..')

from nukleus.model.Footprint import Footprint
from nukleus.SexpParser import load_tree

INPUT_STRING = """  (footprint "Capacitor_THT:CP_Axial_L18.0mm_D6.5mm_P25.00mm_Horizontal" (layer "F.Cu")
    (tedit 5A533291) (tstamp 00000000-0000-0000-0000-000054032b86)
    (at 110.49 78.867 180)
    (descr "CP, Axial series, Axial, Horizontal, pin pitch=25mm, , length*diameter=18*6.5mm^2, Electrolytic Capacitor, , http://www.vishay.com/docs/28325/021asm.pdf")
    (tags "CP Axial series Axial Horizontal pin pitch 25mm  length 18mm diameter 6.5mm Electrolytic Capacitor")
    (property "Sheetfile" "pic_programmer.kicad_sch")
    (property "Sheetname" "")
    (path "/00000000-0000-0000-0000-0000442a5056")
    (attr through_hole)
    (fp_text reference "C1" (at 12.5 -4.31 180) (layer "F.SilkS")
      (effects (font (size 1 1) (thickness 0.15)))
      (tstamp a6f1cee4-350a-49d7-858b-50d3e3d852dc)
    )
    (fp_text value "100µF" (at 12.5 4.31 180) (layer "F.Fab")
      (effects (font (size 1 1) (thickness 0.15)))
      (tstamp 6714d3d0-67c3-4e88-bf4d-4c5f778e0892)
    )
    (fp_text user "${REFERENCE}" (at 12.5 0 180) (layer "F.Fab")
      (effects (font (size 1 1) (thickness 0.15)))
      (tstamp bc27282e-eeb3-4ed4-b421-f3a6eaa2e2b5)
    )
    (fp_line (start 3.38 3.37) (end 5.18 3.37) (layer "F.SilkS") (width 0.12) (tstamp 3462ecc2-1bae-4a89-9f65-63a9e667d09c))
    (fp_line (start 6.98 -3.37) (end 21.62 -3.37) (layer "F.SilkS") (width 0.12) (tstamp 4d1afc95-4219-4bbd-9746-9af92b8382e5))
    (fp_line (start 1.44 0) (end 3.38 0) (layer "F.SilkS") (width 0.12) (tstamp 58df7ef1-b92a-49a0-8639-c0c281311c8c))
    (fp_line (start 5.18 3.37) (end 6.08 2.47) (layer "F.SilkS") (width 0.12) (tstamp 8959f01b-661c-44a4-a6b5-b57e597117d1))
    (fp_line (start 6.08 2.47) (end 6.98 3.37) (layer "F.SilkS") (width 0.12) (tstamp 928467d1-ef81-4aa0-b95a-3562ac729310))
    (fp_line (start 6.08 -2.47) (end 6.98 -3.37) (layer "F.SilkS") (width 0.12) (tstamp 9f77a334-8c05-44eb-8734-b02323623980))
    (fp_line (start 3.38 -3.37) (end 5.18 -3.37) (layer "F.SilkS") (width 0.12) (tstamp a5ffbea5-7343-4e67-95ca-798ecf1a31fd))
    (fp_line (start 2.18 -3.5) (end 2.18 -1.7) (layer "F.SilkS") (width 0.12) (tstamp b2ac688b-7bb5-4f97-83f4-4421e72e5ebf))
    (fp_line (start 23.56 0) (end 21.62 0) (layer "F.SilkS") (width 0.12) (tstamp bffcf4d1-909b-4c58-a5be-6561a7007f9d))
    (fp_line (start 6.98 3.37) (end 21.62 3.37) (layer "F.SilkS") (width 0.12) (tstamp c4dcabfd-61e1-4503-9ff2-b41ab53d91aa))
    (fp_line (start 3.38 -3.37) (end 3.38 3.37) (layer "F.SilkS") (width 0.12) (tstamp d75f58b8-4e6d-4e45-b9c3-b942ded81af0))
    (fp_line (start 5.18 -3.37) (end 6.08 -2.47) (layer "F.SilkS") (width 0.12) (tstamp e0db893c-3ed0-4514-88f8-12392d977eb3))
    (fp_line (start 1.28 -2.6) (end 3.08 -2.6) (layer "F.SilkS") (width 0.12) (tstamp e67045ec-7ac2-4e58-adbd-ba06b515c475))
    (fp_line (start 21.62 -3.37) (end 21.62 3.37) (layer "F.SilkS") (width 0.12) (tstamp e7e8636e-8a1d-4bd2-9304-51c7bf88ca86))
    (fp_line (start 26.45 3.65) (end 26.45 -3.65) (layer "F.CrtYd") (width 0.05) (tstamp 5a03366f-05a8-4568-93d7-90ee54ce1ff3))
    (fp_line (start 26.45 -3.65) (end -1.45 -3.65) (layer "F.CrtYd") (width 0.05) (tstamp e12abc24-3857-4264-8f78-760101a7cc3a))
    (fp_line (start -1.45 -3.65) (end -1.45 3.65) (layer "F.CrtYd") (width 0.05) (tstamp f10e3c6e-61e7-4406-8325-82fe978579b0))
    (fp_line (start -1.45 3.65) (end 26.45 3.65) (layer "F.CrtYd") (width 0.05) (tstamp fe3f3336-5cdc-4945-bb13-258cab45397b))
    (fp_line (start 5.18 -3.25) (end 6.08 -2.35) (layer "F.Fab") (width 0.1) (tstamp 01242f51-9ef5-41ff-8af9-2bdf66835e68))
    (fp_line (start 6.98 -3.25) (end 21.5 -3.25) (layer "F.Fab") (width 0.1) (tstamp 06c3c0e6-7385-4c0b-9f22-d75dd843999d))
    (fp_line (start 6.98 3.25) (end 21.5 3.25) (layer "F.Fab") (width 0.1) (tstamp 09b3b400-f689-4913-9c2a-b2fb5a9c8fe9))
    (fp_line (start 5.2 0) (end 7 0) (layer "F.Fab") (width 0.1) (tstamp 1cd0ab3b-0f4f-4cc1-9e4e-c3de697a4b0c))
    (fp_line (start 0 0) (end 3.5 0) (layer "F.Fab") (width 0.1) (tstamp 370894ef-352b-48a4-96be-27098b7d9461))
    (fp_line (start 3.5 3.25) (end 5.18 3.25) (layer "F.Fab") (width 0.1) (tstamp 3c84e368-3edc-42e0-8982-20119cfb45c2))
    (fp_line (start 5.18 3.25) (end 6.08 2.35) (layer "F.Fab") (width 0.1) (tstamp 58f08ba5-d0e3-43fb-8beb-54efdce75f59))
    (fp_line (start 6.08 -2.35) (end 6.98 -3.25) (layer "F.Fab") (width 0.1) (tstamp 5bf8b68b-0b4d-40fe-a110-744583af3d4a))
    (fp_line (start 3.5 -3.25) (end 3.5 3.25) (layer "F.Fab") (width 0.1) (tstamp 6854b04c-649e-4a30-b3ab-bda4116a5800))
    (fp_line (start 3.5 -3.25) (end 5.18 -3.25) (layer "F.Fab") (width 0.1) (tstamp 8c26551c-34ed-4948-86f2-5130f204da63))
    (fp_line (start 21.5 -3.25) (end 21.5 3.25) (layer "F.Fab") (width 0.1) (tstamp 95b82f4c-5c3b-488f-bcd4-94fa52f1c68a))
    (fp_line (start 25 0) (end 21.5 0) (layer "F.Fab") (width 0.1) (tstamp acf4f9ad-dce8-45ef-b6fe-68166c97c929))
    (fp_line (start 6.08 2.35) (end 6.98 3.25) (layer "F.Fab") (width 0.1) (tstamp b1538173-2109-4b6b-b681-1a93dc0f2cb2))
    (fp_line (start 6.1 -0.9) (end 6.1 0.9) (layer "F.Fab") (width 0.1) (tstamp bbf21b15-3165-4683-902a-e1e739cc2923))
    (pad "1" thru_hole rect locked (at 0 0 180) (size 2.4 2.4) (drill 1.2) (layers *.Cu *.Mask)
      (net 17 "VCC") (pintype "passive") (tstamp d6f6699b-7183-4350-ba44-c47e828a3a04))
    (pad "2" thru_hole oval locked (at 25 0 180) (size 2.4 2.4) (drill 1.2) (layers *.Cu *.Mask)
      (net 2 "GND") (pintype "passive") (tstamp fef03265-6842-4b6b-8bc1-b07c32ea999b))
    (model "${KICAD6_3DMODEL_DIR}/Capacitor_THT.3dshapes/CP_Axial_L18.0mm_D6.5mm_P25.00mm_Horizontal.wrl"
      (offset (xyz 0 0 0))
      (scale (xyz 1 1 1))
      (rotate (xyz 0 0 0))
    )
  )"""


class TestFootprint(unittest.TestCase):

    def test_parse_footprint(self):
        sexp_str = load_tree(INPUT_STRING)
        footprint = Footprint.parse(sexp_str)
        self.assertEqual((110.49, 78.867), footprint.pos)
        self.assertEqual(180, footprint.angle)

#    def test_sexp_footprint(self):
#        sexp_str = load_tree(
#                """  (no_connect (at 115.57 78.74) (uuid eae0ab9f-65b2-44d3-aba7-873c3227fba7))""")
#        symbol_instance = Footprint.parse(sexp_str)
#        self.assertEqual(
#                """  (no_connect (at 115.57 78.74) (uuid eae0ab9f-65b2-44d3-aba7-873c3227fba7))""",
#                symbol_instance.sexp())
