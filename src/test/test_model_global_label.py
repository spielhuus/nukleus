import sys
import unittest

from nukleus.model.GlobalLabel import GlobalLabel
from nukleus.model.Property import Property
from nukleus.model.TextEffects import Justify, TextEffects
from nukleus.SexpParser import load_tree

sys.path.append("src")
sys.path.append("..")


INPUT_STRINGG = """  (global_label "INPUT" (shape input) (at 53.34 43.18 180) (fields_autoplaced)
    (effects (font (size 1.27 1.27)) (justify right))
    (uuid 9cbf35b8-f4d3-42a3-bb16-04ffd03fd8fd)
    (property "Intersheet References" "${INTERSHEET_REFS}" (id 0) (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
  )"""


class TestGlobalLabel(unittest.TestCase):
    def test_parse_global_label(self):
        sexp_str = load_tree(INPUT_STRINGG)
        global_label = GlobalLabel.parse(sexp_str)
        self.assertEqual("INPUT", global_label.text)
        self.assertEqual("input", global_label.shape)
        self.assertEqual((53.34, 43.18), global_label.pos)
        self.assertEqual(180, global_label.angle)
        self.assertEqual("fields_autoplaced", global_label.autoplaced)
        self.assertEqual(
            "9cbf35b8-f4d3-42a3-bb16-04ffd03fd8fd", global_label.identifier
        )
        self.assertEqual(
            TextEffects(
                font_height=1.27, font_width=1.27, hidden=False, justify=[Justify.RIGHT]
            ),
            global_label.text_effects,
        )
        self.assertEqual(
            Property(
                key="Intersheet References",
                value="${INTERSHEET_REFS}",
                id=0,
                pos=(0, 0),
                angle=0,
                text_effects=TextEffects(
                    font_height=1.27,
                    font_width=1.27,
                    hidden=True,
                ),
            ),
            global_label.properties[0],
        )

    def test_new_global_label(self):
        global_label = GlobalLabel(
            identifier="9cbf35b8-f4d3-42a3-bb16-04ffd03fd8fd",
            pos=(53.34, 43.18),
            angle=180,
            text="INPUT",
            shape="input",
            autoplaced="fields_autoplaced",
            text_effects=TextEffects(
                font_height=1.27,
                font_width=1.27,
                hidden=False,
                justify=[Justify.RIGHT],
            ),
            properties=[
                Property(
                    key="Intersheet References",
                    value="${INTERSHEET_REFS}",
                    id=0,
                    pos=(0, 0),
                    angle=0,
                    text_effects=TextEffects(
                        font_height=1.27,
                        font_width=1.27,
                        hidden=True,
                    ),
                ),
            ],
        )
        self.assertEqual("INPUT", global_label.text)
        self.assertEqual("input", global_label.shape)
        self.assertEqual((53.34, 43.18), global_label.pos)
        self.assertEqual(180, global_label.angle)
        self.assertEqual("fields_autoplaced", global_label.autoplaced)
        self.assertEqual(
            "9cbf35b8-f4d3-42a3-bb16-04ffd03fd8fd", global_label.identifier
        )
        self.assertEqual(
            TextEffects(
                font_height=1.27, font_width=1.27, hidden=False, justify=[Justify.RIGHT]
            ),
            global_label.text_effects,
        )
        self.assertEqual(
            Property(
                key="Intersheet References",
                value="${INTERSHEET_REFS}",
                id=0,
                pos=(0, 0),
                angle=0,
                text_effects=TextEffects(
                    font_height=1.27,
                    font_width=1.27,
                    hidden=True,
                ),
            ),
            global_label.properties[0],
        )

    def test_sexp_global_label(self):
        sexp_str = load_tree(INPUT_STRINGG)
        symbol_instance = GlobalLabel.parse(sexp_str)
        self.assertEqual(INPUT_STRINGG, symbol_instance.sexp())
