from sys import path
import unittest
from unittest.mock import patch

import sys
sys.path.append('src')
sys.path.append('../../src')

from nukleus.Schema import Schema
from nukleus.ModelBase import *
from nukleus.ModelSchema import *
from nukleus.ParserVisitor import ParserVisitor
from nukleus.SexpParser import *


class TestKicadModel(unittest.TestCase):

    def test_parse_text_effects(self):
        sexp_str = load_tree(
            """(effects (font (size 1.27 1.27)) (justify right bottom) hide)""")
        text_effects = ParserVisitor._get_text_effects(sexp_str)
        self.assertEqual(1.27, text_effects.font_width)
        self.assertEqual(1.27, text_effects.font_height)
        self.assertEqual(0, text_effects.font_thickness)
        self.assertEqual([], text_effects.font_style)
        self.assertEqual([Justify.RIGHT, Justify.BOTTOM], text_effects.justify)
        self.assertEqual(True, text_effects.hidden)

    def test_parse_text_effects_style(self):
        sexp_str = load_tree(
            """  (effects (font (size 2.54 2.54) (thickness 0.508) bold italic) (justify left bottom))""")
        text_effects = ParserVisitor._get_text_effects(sexp_str)
        self.assertEqual(2.54, text_effects.font_width)
        self.assertEqual(2.54, text_effects.font_height)
        self.assertEqual(0.508, text_effects.font_thickness)
        self.assertEqual(['bold', 'italic'], text_effects.font_style)
        self.assertEqual([Justify.LEFT, Justify.BOTTOM], text_effects.justify)
        self.assertEqual(False, text_effects.hidden)

    def test_parse_stroke_definition(self):
        sexp_str = load_tree(
            """    (stroke (width 0) (type default) (color 0 0 0 0))""")
        stroke = ParserVisitor._get_stroke_definition(sexp_str)
        self.assertEqual(0, stroke.width)
        self.assertEqual('default', stroke.stroke_type)
        self.assertEqual(rgb(0, 0, 0, 0), stroke.color)

    def test_parse_property(self):
        INPUT_STRINGG = """      (property "Value" "TL072" (id 1) (at 0 -5.08 0)
        (effects (font (size 1.27 1.27)) (justify left))
      )"""
        sexp_str = load_tree(INPUT_STRINGG)
        property = ParserVisitor._get_property(sexp_str)
        self.assertEqual((0, -5.08), property.pos)
        self.assertEqual(0, property.angle)
        self.assertEqual('Value', property.key)
        self.assertEqual('TL072', property.value)
        self.assertEqual(1, property.id)
        self.assertEqual(
            TextEffects(font_height=1.27, font_width=1.27,
                        hidden=False, justify=[Justify.LEFT]),
            property.text_effects)

    def test_parse_pin(self):
        INPUT_STRINGG = """    (pin output line (at 7.62 0 180) (length 2.54)
      (name "~" (effects (font (size 1.27 1.27))))
      (number "1" (effects (font (size 1.27 1.27))))
    )"""
        sexp_str = load_tree(INPUT_STRINGG)
        pin = ParserVisitor._get_pin(sexp_str)
        self.assertEqual((7.62, 0), pin.pos)
        self.assertEqual(180, pin.angle)
        self.assertEqual('output', pin.type)
        self.assertEqual('line', pin.style)
        self.assertEqual(2.54, pin.length)
        self.assertEqual(
            ('~', TextEffects(font_height=1.27, font_width=1.27, hidden=False)), pin.name)
        self.assertEqual(
            ('1', TextEffects(font_height=1.27, font_width=1.27, hidden=False)), pin.number)

    def test_parse_local_label(self):
        INPUT_STRINGG = """  (label "IN_1" (at 96.52 45.72 270)
            (effects (font (size 1.27 1.27)) (justify right bottom))
            (uuid d9c6d5d2-0b49-49ba-a970-cd2c32f74c54)
          )"""
        sexp_str = load_tree(INPUT_STRINGG)
        schema = Schema()
        visitor = ParserVisitor(schema)
        with patch.object(Schema, 'visitLocalLabel', return_value=None) as mock_method:
            text_effects = visitor.node('label', sexp_str)
            mock_method.assert_called_once_with(
                LocalLabel(text='IN_1', pos=(96.52, 45.72), angle=270,
                    text_effects=TextEffects(font_height=1.27, font_width=1.27, justify=[
                                             Justify.RIGHT, Justify.BOTTOM], hidden=False),
                    identifier='d9c6d5d2-0b49-49ba-a970-cd2c32f74c54'))

    def test_parse_wire(self):
        sexp_str = load_tree("""  (wire (pts (xy 87.63 156.21) (xy 87.63 158.75))
    (stroke (width 0) (type default) (color 0 0 0 0))
    (uuid 592f25e6-a01b-47fd-8172-3da01117d00a)
  )""")
        schema = Schema()
        visitor = ParserVisitor(schema)
        with patch.object(Schema, 'visitWire', return_value=None) as mock_method:
            wire = visitor.node('wire', sexp_str)
            mock_method.assert_called_once_with(
                Wire(pts=[(87.63, 156.21), (87.63, 158.75)],
                    stroke_definition=StrokeDefinition(
                        width=0, stroke_type='default', color=rgb(0, 0, 0, 0)),
                    identifier='592f25e6-a01b-47fd-8172-3da01117d00a'))

    def test_parse_no_connect(self):
        sexp_str = load_tree(
            """  (no_connect (at 115.57 78.74) (uuid eae0ab9f-65b2-44d3-aba7-873c3227fba7))""")
        schema = Schema()
        visitor = ParserVisitor(schema)
        with patch.object(Schema, 'visitNoConnect', return_value=None) as mock_method:
            wire = visitor.node('no_connect', sexp_str)
            mock_method.assert_called_once_with(
                NoConnect(
                    pos=(115.57, 78.74),
                    angle=0,
                    identifier='eae0ab9f-65b2-44d3-aba7-873c3227fba7'))

    def test_parse_junction(self):
        INPUT_STRINGG = """  (junction (at 93.98 163.83) (diameter 0) (color 0 0 0 0)
            (uuid e3fc1e69-a11c-4c84-8952-fefb9372474e)
          )"""
        sexp_str = load_tree(INPUT_STRINGG)
        schema = Schema()
        visitor = ParserVisitor(schema)
        with patch.object(Schema, 'visitJunction', return_value=None) as mock_method:
            visitor.node('junction', sexp_str)
            mock_method.assert_called_once_with(
                Junction(
                    pos=(93.98, 163.83),
                    angle=0,
                    diameter=0,
                    color=rgb(0, 0, 0, 0),
                    identifier='e3fc1e69-a11c-4c84-8952-fefb9372474e'))

    def test_parse_global_label(self):
        INPUT_STRINGG = """  (global_label "INPUT" (shape input) (at 53.34 43.18 180) (fields_autoplaced)
    (effects (font (size 1.27 1.27)) (justify right))
    (uuid 9cbf35b8-f4d3-42a3-bb16-04ffd03fd8fd)
    (property "Intersheet References" "${INTERSHEET_REFS}" (id 0) (at 0 0 0)
      (effects (font (size 1.27 1.27)) hide)
    )
  )"""
        sexp_str = load_tree(INPUT_STRINGG)
        schema = Schema()
        visitor = ParserVisitor(schema)
        with patch.object(Schema, 'visitGlobalLabel', return_value=None) as mock_method:
            visitor.node('global_label', sexp_str)
            mock_method.assert_called_once_with(
                GlobalLabel(
                    pos=(53.34, 43.18),
                    angle=180,
                    text='INPUT',
                    shape='input',
                    autoplaced=True,
                    text_effects=TextEffects(
                            font_height=1.27, font_width=1.27, hidden=False, justify=[Justify.RIGHT]),
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
                                hidden=True)
                            )],
                    identifier='9cbf35b8-f4d3-42a3-bb16-04ffd03fd8fd'))

    def test_parse_graphical_line(self):
        GRAPHICAL_LINE = """  (polyline (pts (xy 172.72 170.18) (xy 172.72 196.85))
    (stroke (width 0) (type dash) (color 0 0 0 0))
    (uuid 12d34910-9c6c-4880-b730-cafdbf5d87ee)
  )"""
        sexp_str = load_tree(GRAPHICAL_LINE)
        schema = Schema()
        visitor = ParserVisitor(schema)
        with patch.object(Schema, 'visitGraphicalLine', return_value=None) as mock_method:
            visitor.node('polyline', sexp_str)
            mock_method.assert_called_once_with(
                GraphicalLine(
                    pts=[(172.72, 170.18), (172.72, 196.85)],
                    stroke_definition=StrokeDefinition(
                        width=0, stroke_type='dash', color=rgb(0, 0, 0, 0)),
                    identifier='12d34910-9c6c-4880-b730-cafdbf5d87ee'))

    def test_parse_graphical_text(self):
        sexp_str = load_tree(
                """    (text "resistor R25 must be connected to inverting input" (at 38.1 127 0)
    (effects (font (size 1.27 1.27)) (justify left bottom))
    (uuid 22bb6c80-05a9-4d89-98b0-f4c23fe6c1ce)
  )""")
        schema = Schema()
        visitor = ParserVisitor(schema)
        with patch.object(Schema, 'visitGraphicalText', return_value=None) as mock_method:
            visitor.node('text', sexp_str)
            mock_method.assert_called_once_with(
                GraphicalText(
                    text="resistor R25 must be connected to inverting input",
                    text_effects=TextEffects(
                                font_height=1.27,
                                font_width=1.27,
                                hidden=False,
                                justify=[Justify.LEFT, Justify.BOTTOM]),
                    identifier="22bb6c80-05a9-4d89-98b0-f4c23fe6c1ce",
                    pos=(38.1, 127),
                    angle=0))

    def test_parse_sheet_instance(self):
        SHEET_INSTANCE = """(sheet_instances    (path "/" (page "1")))"""
        sexp_str = load_tree(SHEET_INSTANCE)
        schema = Schema()
        visitor = ParserVisitor(schema)
        with patch.object(Schema, 'visitSheetInstance', return_value=None) as mock_method:
            visitor.node('sheet_instances', sexp_str)
            mock_method.assert_called_once_with(
                HierarchicalSheetInstance(page=1, path="/"))

    def test_parse_hierarchical_sheet(self):
        HIERARCHICAL_SHEET = """  (sheet (at 233.68 78.74) (size 39.37 30.48)
    (stroke (width 0) (type solid) (color 0 0 0 0))
    (fill (color 0 0 0 0))
    (uuid 00000000-0000-0000-0000-00004804a5e2)
    (property "Sheet name" "pic_sockets" (id 0) (at 233.68 77.9775 0)
      (effects (font (size 1.524 1.524)) (justify left bottom))
    )
    (property "Sheet file" "pic_sockets.kicad_sch" (id 1) (at 233.68 109.8301 0)
      (effects (font (size 1.524 1.524)) (justify left top))
    )
    (pin "VPP-MCLR" input (at 233.68 88.9 180)
      (effects (font (size 1.524 1.524)) (justify left))
      (uuid 4f5ccd8c-8f94-4906-8b6b-52cfd5ec3797)
    )
  )"""
        sexp_str = load_tree(HIERARCHICAL_SHEET)
        schema = Schema()
        visitor = ParserVisitor(schema)
        with patch.object(Schema, 'visitHierarchicalSheet', return_value=None) as mock_method:
            visitor.node('sheet', sexp_str)
            mock_method.assert_called_once_with(
                HierarchicalSheet(
                    size=[(39.37, 30.48)],
                    fill=rgb(0, 0, 0, 0),
                    stroke_definition=StrokeDefinition(
                        width=0, stroke_type='solid', color=rgb(0, 0, 0, 0)),
                    identifier="00000000-0000-0000-0000-00004804a5e2",
                    pos=(233.68, 78.74),
                    angle=0,
                    properties=[
                        Property(key='Sheet name', value='pic_sockets', id=0, pos=(233.68, 77.9775), angle=0,
                            text_effects=TextEffects(font_height=1.524,
                                font_width=1.524,
                                hidden=False,
                                justify=[Justify.LEFT, Justify.BOTTOM])),
                        Property(key='Sheet file', value='pic_sockets.kicad_sch', id=1, pos=(233.68, 109.8301), angle=0,
                            text_effects=TextEffects(font_height=1.524,
                                font_width=1.524,
                                hidden=False,
                                justify=[Justify.LEFT, Justify.TOP])),
                    ],
                    pins=[
                        HierarchicalSheetPin(pin_type='input', pos=(233.68, 88.9), angle=180,
                            name='VPP-MCLR', identifier='4f5ccd8c-8f94-4906-8b6b-52cfd5ec3797',
                            text_effects=TextEffects(font_height=1.524,
                                font_width=1.524,
                                hidden=False,
                                justify=[Justify.LEFT])),
                    ]))

    def test_parse_hierarchical_label(self):
        HIERARCHICAL_LABEL = """  (hierarchical_label "RAS6-" (shape input) (at 212.09 181.61 180)
    (effects (font (size 1.524 1.524)) (justify right))
    (uuid 2370ec94-b3a1-4a98-8c0a-a183cc2fa704)
  )"""
        sexp_str = load_tree(HIERARCHICAL_LABEL)
        schema = Schema()
        visitor = ParserVisitor(schema)
        with patch.object(Schema, 'visitHierarchicalLabel', return_value=None) as mock_method:
            visitor.node('hierarchical_label', sexp_str)
            mock_method.assert_called_once_with(HierarchicalLabel(
                identifier='2370ec94-b3a1-4a98-8c0a-a183cc2fa704',
                pos=(212.09, 181.61), angle=180.0, text='RAS6-',
                shape=HierarchicalLabelShape.shape('input'), text_effects=TextEffects(
                    face='', font_width=1.524, font_height=1.524, font_thickness=0,
                    font_style=[], justify=[Justify.RIGHT], hidden=False)))

    def test_parse_symbol(self):
        INPUT_STRINGG = """  (symbol (lib_id "Device:R") (at 88.9 33.02 270) (unit 1)
    (in_bom yes) (on_board yes)
    (uuid 00000000-0000-0000-0000-00005ea43020)
    (property "Reference" "R4" (id 0) (at 88.9 27.7622 90))
    (property "Value" "100k" (id 1) (at 88.9 30.0736 90))
    (property "Footprint" "Resistor_SMD:R_0805_2012Metric_Pad1.20x1.40mm_HandSolder" (id 2) (at 88.9 31.242 90)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Datasheet" "~" (id 3) (at 88.9 33.02 0)
      (effects (font (size 1.27 1.27)) hide)
    )
    (property "Description" "Thick Film Resistors - SMD (0805)" (id 4) (at 88.9 33.02 90)
      (effects (font (size 1.27 1.27)) hide)
    )
    (pin "1" (uuid 7f41b6ad-3624-48a6-a0d2-d278e9f52b3d))
    (pin "2" (uuid 5f4fd338-1c9e-4638-abf9-b24cce2a1173))
  )"""
        sexp_str = load_tree(INPUT_STRINGG)
        schema = Schema()
        visitor = ParserVisitor(schema)
        visitor.libraries = {'Device:R': 'R'}
        with patch.object(Schema, 'visitSymbol', return_value=None) as mock_method:
            visitor.node('symbol', sexp_str)
            mock_method.assert_called_once_with(
                Symbol(
                identifier='00000000-0000-0000-0000-00005ea43020',
                pos=(88.9, 33.02),
                angle=270,
                mirror='',
                library_identifier='Device:R',
                unit=1,
                in_bom=True,
                on_board=True,
                on_schema=True,
                properties=[
                    Property(key='Reference', value='R4', id=0, pos=(88.9, 27.7622), angle=90, text_effects=None),
                    Property(key='Value', value='100k', id=1, pos=(88.9, 30.0736), angle=90, text_effects=None),
                    Property(key='Footprint',
                             value='Resistor_SMD:R_0805_2012Metric_Pad1.20x1.40mm_HandSolder',
                             id=2, pos=(88.9, 31.242), angle=90,
                             text_effects=TextEffects(font_width=1.27, font_height=1.27, hidden=True)),
                    Property(key='Datasheet', value='~', id=3,
                             pos=(88.9, 33.02), angle=0,
                             text_effects=TextEffects(font_width=1.27, font_height=1.27, hidden=True)),
                    Property(key='Description', value='Thick Film Resistors - SMD (0805)',
                             id=4, pos=(88.9, 33.02), angle=90,
                             text_effects=TextEffects(font_width=1.27, font_height=1.27, hidden=True)),
                ],
                pins=[
                    PinRef(number="1", identifier='7f41b6ad-3624-48a6-a0d2-d278e9f52b3d'),
                    PinRef(number="2", identifier='5f4fd338-1c9e-4638-abf9-b24cce2a1173'),
                ],
                library_symbol='R'
                ))

    def test_parse_library_symbol(self):
        INPUT_STRINGG = """(lib_symbols    (symbol "Device:R" (pin_numbers hide) (pin_names (offset 0)) (in_bom yes) (on_board yes)
      (property "Reference" "R" (id 0) (at 2.032 0 90)
        (effects (font (size 1.27 1.27)))
      )
      (property "Value" "R" (id 1) (at 0 0 90)
        (effects (font (size 1.27 1.27)))
      )
      (property "Footprint" "" (id 2) (at -1.778 0 90)
        (effects (font (size 1.27 1.27)) hide)
      )
      (property "Datasheet" "~" (id 3) (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (property "ki_keywords" "R res resistor" (id 4) (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (property "ki_description" "Resistor" (id 5) (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (property "ki_fp_filters" "R_*" (id 6) (at 0 0 0)
        (effects (font (size 1.27 1.27)) hide)
      )
      (symbol "R_0_1"
        (rectangle (start -1.016 -2.54) (end 1.016 2.54)
          (stroke (width 0.254) (type default) (color 0 0 0 0))
          (fill (type none))
        )
      )
      (symbol "R_1_1"
        (pin passive line (at 0 3.81 270) (length 1.27)
          (name "~" (effects (font (size 1.27 1.27))))
          (number "1" (effects (font (size 1.27 1.27))))
        )
        (pin passive line (at 0 -3.81 90) (length 1.27)
          (name "~" (effects (font (size 1.27 1.27))))
          (number "2" (effects (font (size 1.27 1.27))))
        )
      )
    ))"""
        sexp_str = load_tree(INPUT_STRINGG)
        schema = Schema()
        visitor = ParserVisitor(schema)
        with patch.object(Schema, 'visitLibrarySymbol', return_value=None) as mock_method:
            visitor.node('lib_symbols', sexp_str)
            mock_method.assert_called_once_with(
                LibrarySymbol(
                    identifier="Device:R",
                    pin_numbers_hide=True,
                    pin_names_hide=False,
                    pin_names_offset=0,
                    in_bom=True,
                    on_board=True,
                    properties=[
                        Property(key='Reference', value='R',
                                 id=0, pos=(2.032, 0), angle=90,
                                 text_effects=TextEffects(font_width=1.27, font_height=1.27, hidden=False)),
                        Property(key='Value', value='R',
                                 id=1, pos=(0, 0), angle=90,
                                 text_effects=TextEffects(font_width=1.27, font_height=1.27, hidden=False)),
                        Property(key='Footprint', value='',
                                 id=2, pos=(-1.778, 0), angle=90,
                                 text_effects=TextEffects(font_width=1.27, font_height=1.27, hidden=True)),
                        Property(key='Datasheet', value='~',
                                 id=3, pos=(0, 0), angle=0,
                                 text_effects=TextEffects(font_width=1.27, font_height=1.27, hidden=True)),
                        Property(key='ki_keywords', value='R res resistor',
                                 id=4, pos=(0, 0), angle=0,
                                 text_effects=TextEffects(font_width=1.27, font_height=1.27, hidden=True)),
                        Property(key='ki_description', value='Resistor',
                                 id=5, pos=(0, 0), angle=0,
                                 text_effects=TextEffects(font_width=1.27, font_height=1.27, hidden=True)),
                        Property(key='ki_fp_filters', value='R_*',
                                 id=6, pos=(0, 0), angle=0,
                                 text_effects=TextEffects(font_width=1.27, font_height=1.27, hidden=True)),
                    ],
                    units=[
                        LibrarySymbol(identifier='R_0_1',
                            graphics=[
                                Rectangle(start_x=-1.016, start_y=-2.54, end_x=1.016, end_y=2.54,
                                    stroke_definition=StrokeDefinition(
                                        width=0.254, stroke_type='default', color=rgb(0, 0, 0, 0)),
                                    fill=FillType.NONE),
                            ]),
                        LibrarySymbol(identifier='R_1_1',
                            pins=[
                                Pin(type='passive', style='line', pos=(0, 3.81), angle=270, length=1.27,
                                    name=('~', TextEffects(font_width=1.27, font_height=1.27, hidden=False)),
                                    number=('1', TextEffects(font_width=1.27, font_height=1.27, hidden=False))),
                                Pin(type='passive', style='line', pos=(0, -3.81), angle=90, length=1.27,
                                    name=('~', TextEffects(font_width=1.27, font_height=1.27, hidden=False)),
                                    number=('2', TextEffects(font_width=1.27, font_height=1.27, hidden=False))),
                            ])
                    ]))

    def test_parse_symbol_instance(self):
        sexp_str = load_tree("""(symbol_instances    (path "/00000000-0000-0000-0000-000061bc0ef5"
          (reference "C1") (unit 1) (value "0.1u") (footprint "Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder")
        ))""")
        schema = Schema()
        visitor = ParserVisitor(schema)
        with patch.object(Schema, 'visitSymbolInstance', return_value=None) as mock_method:
            visitor.node('symbol_instances', sexp_str)
            mock_method.assert_called_once_with(
                SymbolInstance(path='/00000000-0000-0000-0000-000061bc0ef5',
                               reference='C1',
                               unit=1,
                               value='0.1u',
                               footprint='Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder',
                               identifier='/00000000-0000-0000-0000-000061bc0ef5'))

    def test_parse_bus(self):
        sexp_str = load_tree("""  (bus (pts (xy 327.66 111.76) (xy 351.79 111.76))
    (stroke (width 0) (type solid) (color 0 0 0 0))
    (uuid 0c753b9e-5f93-4479-b1a6-b98503e7ca25)
  )""")

        schema = Schema()
        visitor = ParserVisitor(schema)
        with patch.object(Schema, 'visitBus', return_value=None) as mock_method:
            visitor.node('bus', sexp_str)
            mock_method.assert_called_once_with(Bus(
                identifier='0c753b9e-5f93-4479-b1a6-b98503e7ca25',
                pts=[(327.66, 111.76), (351.79, 111.76)],
                stroke_definition=StrokeDefinition(width=0.0, stroke_type='solid',
                    color=rgb(0, 0, 0, 0))))

    def test_parse_bus_entry(self):
        sexp_str = load_tree("""  (bus_entry (at 140.97 161.29) (size 2.54 -2.54)
    (stroke (width 0.1524) (type solid) (color 0 0 0 0))
    (uuid ca2cc51e-1efa-48be-969c-d8fb55c8b635)
  )""")
        schema = Schema()
        visitor = ParserVisitor(schema)
        with patch.object(Schema, 'visitBusEntry', return_value=None) as mock_method:
            visitor.node('bus_entry', sexp_str)
            mock_method.assert_called_once_with(BusEntry(
                identifier='ca2cc51e-1efa-48be-969c-d8fb55c8b635',
                pos=(140.97, 161.29), angle=0.0, size=[(2.54, -2.54)],
                stroke_definition=StrokeDefinition(
                    width=0.1524, stroke_type='solid', color=rgb(0, 0, 0, 0))))

