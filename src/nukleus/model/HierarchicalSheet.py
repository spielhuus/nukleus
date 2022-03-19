from __future__ import annotations

from typing import List, Tuple, cast

from .Utils import ffmt
from .StrokeDefinition import StrokeDefinition, rgb
from .SchemaElement import POS_T, PTS_T
from .PositionalElement import PositionalElement
from .Property import Property
from .Pin import Pin
from .HierarchicalSheetPin import HierarchicalSheetPin
from ..SexpParser import SEXP_T


class HierarchicalSheet(PositionalElement):
    """
    The sheet token defines a hierarchical sheet of the schematic.
    """
    def __init__(self, **kwargs) -> None:
        self.size: PTS_T =  kwargs.get('size', (0, 0))
        """The size token attributes define the WIDTH and HEIGHT of the sheet."""
        self.stroke_definition: StrokeDefinition = \
            kwargs.get('stroke_definition', StrokeDefinition())
        """The STROKE_DEFINITION defines how the sheet outline is drawn."""
        self.properties: List[Property] = kwargs.get('properties', [])
        """The SHEET_PROPERTY_NAME and FILE_NAME_PROPERTY are properties that defines the name
        and filename of the sheet. These properties are mandatory."""
        self.pins: List[Pin] =  kwargs.get('pins', [])
        """The HIERARCHICAL_PINS section is a list of hierarchical pins
        that map a hierarchical label defined in the associated schematic file."""
        self.fill: rgb =  kwargs.get('fill', rgb(0, 0, 0, 0))
        """The FILL_DEFINITION defines how the sheet is filled."""
        super().__init__(kwargs.get('identifier', None),
                         kwargs.get('pos', (0, 0)),
                         kwargs.get('angle', 0))

    @classmethod
    def parse(cls, sexp: SEXP_T) -> HierarchicalSheet:
        """Parse the sexp input.

        :param sexp SEXP_T: Sexp as List.
        :rtype HierarchicalSheet: The HierarchicalSheet Object.
        """
        _pos: POS_T = (0, 0)
        _angle: float = 0
        _size: Tuple[float, float] = (0, 0)
        _identifier: str|None = None
        _stroke_definition: StrokeDefinition = StrokeDefinition()
        _properties: List[Property] = []
        _pins: List[HierarchicalSheetPin] = []
        _fill: rgb = rgb(0, 0, 0, 0)

        for token in sexp[1:]:
            if token[0] == 'at':
                _pos = (float(token[1]), float(token[2]))
                if len(token) == 4:
                    _angle = float(token[3])
            elif token[0] == 'uuid':
                _identifier = token[1]
            elif token[0] == 'size':
                _size = (float(token[1]), float(token[2]))
            elif token[0] == 'stroke':
                _stroke_definition = StrokeDefinition.parse(cast(SEXP_T, token))
            elif token[0] == 'property':
                _properties.append(Property.parse(cast(SEXP_T, token)))
            elif token[0] == 'pin':
                _pins.append(HierarchicalSheetPin.parse(cast(SEXP_T, token)))
            elif token[0] == 'fill' and token[1][0] == 'color':
                _fill = rgb(float(token[1][1]), float(token[1][2]),
                            float(token[1][3]), float(token[1][4]))
            else:
                raise ValueError(f"unknown HierarchicalSheet element {token}")

        return HierarchicalSheet(pos=_pos, angle=_angle, size=_size, identifier=_identifier,
                                 stroke_definition=_stroke_definition, properties=_properties,
                                 pins=_pins, fill=_fill)

    def sexp(self, indent: int=1) -> str:
        """
        Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        strings: List[str] = []
        strings.append(f'{"  " * indent}(sheet (at {self.pos[0]} {self.pos[1]}) '
                       f'(size {self.size[0]} {self.size[1]})')
        strings.append(self.stroke_definition.sexp(indent=indent+1))
        strings.append(f'{"  " * (indent + 1)}(fill (color {ffmt(self.fill.r)} '
                       f'{ffmt(self.fill.g)} {ffmt(self.fill.b)} {ffmt(self.fill.a)}))')
        strings.append(f'{"  " * (indent + 1)}(uuid {self.identifier})')
        for prop in self.properties:
            strings.append(prop.sexp(indent=indent+1))
        for pin in self.pins:
            strings.append(pin.sexp(indent=indent+1))
        strings.append(f'{"  " * indent})')
        return "\n".join(strings)
