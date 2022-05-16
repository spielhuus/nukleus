from __future__ import annotations
from abc import ABC
from typing import Any, Dict, List, Tuple, cast
from dataclasses import dataclass, field
import string

from copy import deepcopy
from enum import Enum
import re
import uuid

from .ModelBase import StrokeDefinition, TextEffects, FillType, rgb, BaseElement

import numpy as np
import math

from .Typing import POS_T, PTS_T


###############################################################################
###        the classes for the different types of schema graphics           ###
###############################################################################


@dataclass(kw_only=True)
class GraphicItem():
    """Abstract Class for a GraphicItem."""
    fill: FillType = FillType.NONE


@dataclass(kw_only=True)
class Polyline(GraphicItem):
    '''
    Polyline
    Draw a polyline.

    args:
        :arg fill FillType: fill type
        :arg points Tuple[float, float]: Coordinates of the line
        :arg stroke_definition StrokeDefinition: Line description.
    '''
    points: PTS_T = field(default_factory=list)
    stroke_definition: StrokeDefinition = StrokeDefinition()


@dataclass(kw_only=True)
class Rectangle(GraphicItem):
    """The rectangle token defines a graphical rectangle in a symbol definition."""
    start_x: float = 0
    start_y: float = 0
    end_x: float = 0
    end_y: float = 0
    stroke_definition: StrokeDefinition = StrokeDefinition()


@dataclass(kw_only=True)
class Circle(GraphicItem):
    """ The circle token defines a graphical circle in a symbol definition. """

    center: POS_T = (0, 0)
    radius: float = 0
    stroke_definition: StrokeDefinition = StrokeDefinition()


@dataclass(kw_only=True)
class Arc(GraphicItem):
    """ The arc token defines a graphical arc in a symbol definition. """

    start: POS_T = (0, 0)
    mid: POS_T = (0, 0)
    end: POS_T = (0, 0)
    stroke_definition: StrokeDefinition = StrokeDefinition()


@dataclass(kw_only=True)
class Text(GraphicItem):
    """The text token defines graphical text in a symbol definition."""

    pos: POS_T = (0, 0)
    angle: float = 0
    text: str = ''
    text_effects: TextEffects = TextEffects()


###############################################################################
###        the classes for the different schema graphics elements           ###
###############################################################################

@dataclass(kw_only=True)
class SchemaElement(BaseElement):
    """Base element for the schematic items."""

    identifier: str = ''
    """The UNIQUE_IDENTIFIER defines the universally unique identifier for the pin."""

    def __post_init__(self):
        if self.identifier == '':
            self.identifier = str(uuid.uuid4())

@dataclass(kw_only=True)
class PositionalElement(SchemaElement):
    """ Positional element for the schema items """

    pos: POS_T = (0, 0)
    """The POSITION_IDENTIFIER defines the X and Y coordinates of the element in the sheet."""
    angle: float = 0.0
    """The POSITION_IDENTIFIER defines the angle of rotation of the element in the sheet."""


@dataclass(kw_only=True)
class Pin():
    """
    The pin token defines a pin in a symbol definition.
    """
    type: str = ''
    style: str = ''
    pos: POS_T = (0, 0)
    angle: int = 0
    hidden: bool = False
    length: int = 0
    name: Tuple[str, TextEffects] = ('~', TextEffects())
    number: Tuple[str, TextEffects] = ('0', TextEffects())

#    def _pos(self) -> POS_T:
#        theta = np.deg2rad(self.angle)
#        rot = np.array([math.cos(theta), math.sin(theta)])
#        verts = np.array([self.pos, self.pos + rot * self.length])
#        verts = np.round(verts, 3)
#        return verts

    def calc_pos(self, pos: POS_T, offset: float=0) -> POS_T:
        theta = np.deg2rad(self.angle)
        rot = np.array([math.cos(theta), math.sin(theta)])
        verts = np.array([pos, pos + rot * self.length + offset])
        verts = np.round(verts, 3)
        return verts


class PinImpl(Pin):
    def __init__(self, parent: Symbol, pin: Pin):
        super().__init__(type=pin.type, style=pin.style, pos=pin.pos, angle=pin.angle,
                         length=pin.length, hidden=pin.hidden, name=pin.name, number=pin.number)
        self.parent = parent

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, PinImpl):
            return False
        other_pin = cast(PinImpl, __o)
        return(self.parent.identifier == other_pin.parent.identifier and
               self.number == other_pin.number)

class PinList():
    def __init__(self):
        self.dict: Dict = {}

    def append(self, parent: Symbol, item: Pin):
        self.dict[item.number[0]] = PinImpl(parent, item)

    def extend(self, parent: Symbol, pins: List[Pin]):
        for pin in pins:
            self.dict[pin.number[0]] = PinImpl(parent, pin)

    def __iter__(self):
        ''' Returns the Iterator object '''
        return iter(self.dict.values())

    def __len__(self):
        return len(self.dict)

    def __getitem__(self, key: str):
        assert key in self.dict, f'key not in PinList: {key} {self.dict.keys()}'
        return self.dict[key]

@dataclass(kw_only=True)
class PinRef():
    number: str = ''
    identifier: str = ''
    """Sympol Pin Reference"""

    def sexp(self, indent=1) -> str:
        return f'{"  " * indent}(pin "{self.number}" (uuid {self.identifier}))'


@dataclass(kw_only=True)
class Property:
    """
    The property token defines a key value pair for storing user defined information.
    """

    key: str = ""
    """The "KEY" string defines the name of the property and must be unique."""
    value: str = ""
    """The "VALUE" string defines the value of the property."""
    pos: POS_T = (0, 0)
    """The POSITION_IDENTIFIER defines the X and Y coordinates
    of the property."""
    angle: float = 0
    """The angle defines the rotation angle of the property."""
    id: int = 0
    """The id token defines an integer ID for the property and must be unique."""
    text_effects: TextEffects|None = None
    """The TEXT_EFFECTS section defines how the text is displayed."""


@dataclass(kw_only=True)
class BusEntry(PositionalElement):

    """
    The bus_entry token defines a bus entry in the schematic.
    The bus entry section will not exist if there are no bus
    entries in the schematic.
    """

    size: PTS_T = field(default_factory=list)
    """The size token attributes define the X and Y distance of
    the end point from the position of the bus entry."""
    stroke_definition: StrokeDefinition = StrokeDefinition()


@dataclass(kw_only=True)
class Bus(SchemaElement):
    """
    The bus tokens define wires and buses in the schematic.
    This section will not exist if there are no buses
    in the schematic.
    """

    pts: PTS_T = field(default_factory=list)
    """The COORDINATE_POINT_LIST defines the list of X and Y
    coordinates of start and end points of the wire or bus."""
    stroke_definition: StrokeDefinition = StrokeDefinition()
    """The STROKE_DEFINITION defines how the wire or bus is drawn."""


@dataclass(kw_only=True)
class GlobalLabel(PositionalElement):
    """
    The global_label token defines a label name that is visible across all
    schematics in a design. This section will not exist if no global labels
    are defined in the schematic.
    """

    text: str = ""
    """The TEXT is a quoted string that defines the global label."""
    shape: str = ""
    """The shape token attribute defines the way the global label
    is drawn. See table below for global label shapes."""
    autoplaced: bool = False
    """The optional fields_autoplaced is a flag that indicates
    that any PROPERTIES associated with the global label
    have been place automatically."""
    text_effects: TextEffects = TextEffects()
    """The TEXT_EFFECTS section defines how the global label text is drawn."""
    properties: List[Property] = field(default_factory=list)
    """The PROPERTIES section defines the properties of the global label.
    Currently, the only supported property is the inter-sheet reference."""


@dataclass(kw_only=True)
class GraphicalLine(SchemaElement):
    """
    The polyline token defines one or more lines that may or may not represent
    a polygon. This section will not exist if there are no lines in the schematic.
    """

    pts: PTS_T = field(default_factory=list)
    """The COORDINATE_POINT_LIST defines the list of X/Y coordinates of to draw
    line(s) between. A minimum of two points is required."""
    stroke_definition: StrokeDefinition = StrokeDefinition()


@dataclass(kw_only=True)
class GraphicalText(PositionalElement):
    """
    The text token defines graphical text in a schematic.
    """

    text: str = ''
    """The TEXT is a quoted string that defines the text."""
    text_effects: TextEffects = TextEffects()


@dataclass(kw_only=True)
class HierarchicalLabelShape(Enum):
    """
    Shape tokens global labels, hierarchical labels, and hierarchical sheet pins.
    """
    INPUT = 1
    OUTPUT = 2
    BIDIRECTIONAL = 3
    TRI_STATE = 4
    PASSIVE = 5

    @classmethod
    def string(cls, shape: HierarchicalLabelShape) -> str:
        """
        HierarchicalLabel shape as string.

        :param shape HierarchicalLabelShape: The Shape.
        :rtype str: Shape as string.
        """
        mappings = {
            HierarchicalLabelShape.INPUT: 'input',
            HierarchicalLabelShape.OUTPUT: 'output',
            HierarchicalLabelShape.BIDIRECTIONAL: 'bidirectional',
            HierarchicalLabelShape.TRI_STATE: 'tri_state',
            HierarchicalLabelShape.PASSIVE: 'passive',
            }
        return mappings[shape]

    @classmethod
    def shape(cls, shape: str) -> HierarchicalLabelShape:
        """
        Parse HierarchicalLabel.

        :param shape str: Shape as string.
        :rtype HierarchicalLabelShape: Shape Enum.
        """
        mappings = {
            'input': HierarchicalLabelShape.INPUT,
            'output': HierarchicalLabelShape.OUTPUT,
            'bidirectional': HierarchicalLabelShape.BIDIRECTIONAL,
            'tri_state': HierarchicalLabelShape.TRI_STATE,
            'passive': HierarchicalLabelShape.PASSIVE,
            }
        return mappings[shape]

@dataclass(kw_only=True)
class HierarchicalLabel(PositionalElement):
    """
    The hierarchical_label section defines labels that are used by hierarchical
    sheets to define connections between sheet in hierarchical designs. This
    section will not exist if no global labels are defined in the schematic.
    """

    text: str = ''
    """The TEXT is a quoted string that defines the hierarchical label."""
    shape: HierarchicalLabelShape = HierarchicalLabelShape.INPUT
    """The shape token attribute defines the way the hierarchical label
    is drawn. See table below for hierarchical label shapes."""
    text_effects: TextEffects = TextEffects()
    """The TEXT_EFFECTS section defines how the hierarchical label text is drawn."""


@dataclass(kw_only=True)
class HierarchicalSheetInstance(BaseElement):
    """ The symbol_instance token defines the per symbol information
        for the entire schematic. This section will only exist in
        schematic files that are the root sheet of a project.

    Parameters:
	    The INSTANCE_PATH attribute is the path to the sheet instance.
        The reference token attribute is a string that defines the reference designator for the symbol instance.
        The unit token attribute is a integer ordinal that defines the symbol unit for the symbol instance. For symbols that do not define multiple units, this will always be 1.
        The value token attribute is a string that defines the value field for the symbol instance.
        The footprint token attribute is a string that defines the LIBRARY_IDENTIFIER for footprint associated with the symbol instance.
    """
    path: str = ''
    page: int = 0


@dataclass(kw_only=True)
class HierarchicalSheetPin(PositionalElement):
    """
    The pin token in a sheet object defines an electrical connection between
    the sheet in a schematic with the hierarchical label defined in the
    associated schematic file.
    """

    name: str = ''
    """The "NAME" attribute defines the name of the sheet pin. It must have
    an identically named hierarchical label in the associated schematic file."""
    pin_type: str = ''
    """The electrical connect type token defines the type of electrical
    connect made by the sheet pin."""
    text_effects: TextEffects = TextEffects()


@dataclass(kw_only=True)
class HierarchicalSheet(PositionalElement):
    """
    The sheet token defines a hierarchical sheet of the schematic.
    """
    size: PTS_T = field(default_factory=list)
    """The size token attributes define the WIDTH and HEIGHT of the sheet."""
    stroke_definition: StrokeDefinition = StrokeDefinition()
    """The STROKE_DEFINITION defines how the sheet outline is drawn."""
    properties: List[Property] = field(default_factory=list)
    """The SHEET_PROPERTY_NAME and FILE_NAME_PROPERTY are properties that defines the name
    and filename of the sheet. These properties are mandatory."""
    pins: List[HierarchicalSheetPin] = field(default_factory=list)
    """The HIERARCHICAL_PINS section is a list of hierarchical pins
    that map a hierarchical label defined in the associated schematic file."""
    fill: rgb = rgb(0, 0, 0, 0)
    """The FILL_DEFINITION defines how the sheet is filled."""


@dataclass(kw_only=True)
class Image(SchemaElement):
    pts: List[Tuple[float, float]]
    scale: float = 0.0
    image_data: str = ''

#    @classmethod
#    def parse(cls) -> Image:
#
#        # TODO ID
#        return Image('lskdfj', [(0, 0), (0, 0)], 1, '')


@dataclass(kw_only=True)
class Junction(PositionalElement):
    """
    The junction token defines a junction in the schematic. The junction
    section will not exist if there are no junctions in the schematic.
    """
    diameter: float = 0
    """he diameter token attribute defines the DIAMETER of the junction.
    A diameter of 0 is the default diameter in the system settings."""
    color: rgb = rgb(0, 0, 0, 0)
    """The color token attributes define the Red, Green, Blue, and Alpha
    transparency of the junction. If all four attributes are 0, the
    default junction color is used."""


@dataclass(kw_only=True)
class LibrarySymbol(SchemaElement):
    """
    The symbol token defines a symbol or sub-unit of a parent symbol.
    There can be zero or more symbol tokens in a symbol library.
    """

    identifier: str = ''
    """Each symbol must have a unique "LIBRARY_ID" for each top level symbol
    in the library or a unique "UNIT_ID" for each unit embedded in a parent
    symbol. Library identifiers are only valid it top level symbols and unit
    identifiers are on valid as unit symbols inside a parent symbol."""
    extends: str = ''
    """The optional extends token attribute defines the "LIBRARY_ID" of another
    symbol inside the current library from which to derive a new symbol.
    Extended symbols currently can only have different SYMBOL_PROPERTIES
    than their parent symbol."""
    pin_numbers_hide: bool = False
    """The optional pin_numbers token defines the visibility setting of
    the symbol pin numbers for the entire symbol. If not defined, the
    all of the pin numbers in the symbol are visible."""
    pin_names_offset: float = -1
    """The optional offset token defines the pin name offset for all pin
    names of the symbol. If not defined, the pin name offset is 0.508mm (0.020")."""
    pin_names_hide: bool = False
    """The optional pin_names token defines the visibility for all of the
    pin names of the symbol"""
    in_bom: bool = False
    """The in_bom token, defines if a symbol is to be include in the
    bill of material output. The only valid attributes are yes and no."""
    on_board: bool = False
    """The on_board token, defines if a symbol is to be exported from the
    schematic to the printed circuit board. The only valid attributes are yes and no."""
    properties: List[Property] = field(default_factory=list)
    """The SYMBOL_PROPERTIES is a list of properties that define the symbol.
    The following properties are mandatory when defining a parent symbol:
        -"Reference",
        -"Value",
        -"Footprint",
        -"Datasheet".
    All other properties are optional. Unit symbols cannot have any properties."""
    graphics: List[GraphicItem] = field(default_factory=list)
    """The GRAPHIC ITEMS section is list of graphical arcs, circles, curves, lines,
    polygons, rectangles and text that define the symbol drawing.
    This section can be empty if the symbol has no graphical items."""
    pins: List[Pin] = field(default_factory=list)
    """The PINS section is a list of pins that are used by the symbol.
    This section can be empty if the symbol does not have any pins."""
    units: List[LibrarySymbol] = field(default_factory=list)
    """The optional UNITS can be one or more child symbol tokens
    embedded in a parent symbol."""

    def units_count(self) -> int:
        """return the number of units for the symbol."""
        _count = []
        for unit in self.units:
            *_, lib_unit, _ = unit.identifier.split('_')
            if lib_unit not in _count:
                _count.append(lib_unit)
        return len(_count)-1

@dataclass(kw_only=True)
class LocalLabel(PositionalElement):
    """
    The label token defines an wire or bus label name in a schematic.
    """

    text: str = ''
    """The TEXT is a quoted string that defines the label."""
    text_effects: TextEffects = TextEffects()
    """The TEXT_EFFECTS section defines how the label text is drawn."""


@dataclass(kw_only=True)
class NoConnect(PositionalElement):
    """
    The no_connect token defines a unused pin connection in the schematic.
    The no connect section will not exist if there are not any no connect
    in the schematic.
    """

@dataclass(kw_only=True)
class Symbol(PositionalElement):
    """Symbol Object.
        The Symbol Object represents an instance of a LibrarySymbol.
    """
    mirror: str = ''
    library_identifier: str = ''
    unit: int = 0
    in_bom: bool = True
    on_board: bool = True
    on_schema: bool = True
    autoplaced: bool = False
    properties: List[Property] = field(default_factory=list)
    pins: List[PinRef] = field(default_factory=list)
    library_symbol: LibrarySymbol|None = None

    def property(self, name: str) -> Property:
        """
        Get Property by key.

        :param name str: The Property Key.
        :rtype Property: The Property.
        :raises LookupError: When the property does not exist.
        """
        for prop in self.properties:
            if prop.key == name:
                return prop
        raise LookupError(f"property not found: {name}")

    def has_property(self, name: str) -> bool:
        """
        Test if the Sybol has property by key.

        :param name str: The Property Key.
        :rtype bool: True if the Property exists.
        """
        for prop in self.properties:
            if prop.key == name:
                return True
        return False

    def reference(self):
        """Get the reference of the symbol with the unit as letter."""
        assert self.library_symbol, "library symbol is not set"
        if self.library_symbol.extends == 'power':
            return self.library_identifier.split(":")[1]
        if self.library_symbol.units_count() > 1:
            return f'{self.property("Reference").value}{string.ascii_lowercase[self.unit-1]}'
        return self.property('Reference').value

    @classmethod
    def new(cls, ref: str, lib_name: str, library_symbol: LibrarySymbol, unit: int = 1) -> Symbol:
        """
        Create a new Symbol.
        The new symbol unit is created from the library symbol.
        The lib_name overwrites the library_name.

        :param ref str: Reference of the Symbol.
        :param lib_name str: Library name.
        :param library_symbol LibrarySymbol: Library Symbol
        :param unit int: Unit number
        :rtype Symbol: New symbol instance.
        """
        assert library_symbol, "library symbol not set"
        pins = []
        properties = []
        for prop in library_symbol.properties:
            if not prop.key.startswith('ki_'):
                sym_property = deepcopy(prop)
                if not sym_property.text_effects:
                    sym_property.text_effects = TextEffects(hidden=False)
                if prop.key == 'Reference':
                    sym_property.value = ref
                properties.append(sym_property)

        for sub in library_symbol.units:
            *_, lib_unit, _ = sub.identifier.split('_')
            if lib_unit == '0' or lib_unit == str(unit):
                for pin in sub.pins:
                    pins.append(PinRef(number=pin.number[0], identifier="uuid"))

        sym = Symbol(library_identifier=lib_name, unit=unit,
                     properties=properties,
                     pins=pins, library_symbol=library_symbol)
        return sym

@dataclass(kw_only=True)
class SymbolInstance(SchemaElement):
    """
    The symbol_instance token defines the per symbol information
    for the entire schematic. This section will only exist in
    schematic files that are the root sheet of a project.

    Parameters:
	    The INSTANCE_PATH attribute is the path to the sheet instance.
        The reference token attribute is a string that defines the reference designator for the symbol instance.
        The unit token attribute is a integer ordinal that defines the symbol unit for the symbol instance. For symbols that do not define multiple units, this will always be 1.
        The value token attribute is a string that defines the value field for the symbol instance.
        The footprint token attribute is a string that defines the LIBRARY_IDENTIFIER for footprint associated with the symbol instance.
    """
    path: str = ''
    reference: str = ''
    unit: int = 0
    value: str = ''
    footprint: str = ''


@dataclass(kw_only=True)
class Wire(SchemaElement):
    """
    The wire tokens define wires in the schematic. This section will not
    exist if there are no wires in the schematic.
    """
    pts: PTS_T = field(default_factory=list)
    """The COORDINATE_POINT_LIST defines the list of X and Y
    coordinates of start and end points of the wire."""
    stroke_definition: StrokeDefinition = StrokeDefinition()
    """The STROKE_DEFINITION defines how the wire or bus is drawn."""

def isUnit(symbol: LibrarySymbol, unit: int) -> bool:
    """
    Test if LibrarySymbol is the given unit.

    :param symbol LibrarySymbol: The Library Sub-Symbol.
    :param unit int: The unit number.
    :rtype bool: True if the unit matches.
    """
    match = re.match(r".*_(\d+)_\d+", symbol.identifier)
    if match:
        _unit = int(match.group(1))
        return _unit in (0, (1 if unit == 0 else unit))
    return False
