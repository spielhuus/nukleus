from __future__ import annotations

from dataclasses import dataclass
from typing import List

import uuid

from .FillType import FillType
from .StrokeDefinition import StrokeDefinition, rgb
from .PositionalElement import PositionalElement, POS_T
from .Property import Property
from .Pin import Pin


@dataclass
class HierarchicalSheet(PositionalElement):
    """
    The sheet token defines a hierarchical sheet of the schematic.
    """
    size: POS_T
    autoplaced: str
    stroke_definition: StrokeDefinition
    #fill: FillType
    fill: rgb
    sheetname: Property
    filename: Property
    pins: List[Pin]

    @classmethod
    def new(cls):
        """
        Create a new HierarchicalSheet object.
        """
        return HierarchicalSheet(str(uuid.uuid4()), (0, 0), 0, (0, 0), 'output',
                                 StrokeDefinition.new(),
                                 rgb(0, 0, 0, 0),
                                 Property.new('Sheet name', ''),
                                 Property.new('Sheet file', ''),
                                 [])

    def sexp(self, indent: int=1) -> str:
        """
        Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        strings: List[str] = []
        strings.append(f'{"  " * indent}(sheet (at {self.pos[0]} {self.pos[1]}) (size {self.size[0]} {self.size[1]})')
        strings.append(self.stroke_definition.sexp(indent=indent+1))
        strings.append(f'{"  " * (indent + 1)}(fill (color {self.fill.r} {self.fill.g} {self.fill.b} {self.fill.a}))')
        strings.append(f'{"  " * (indent + 1)}(uuid {self.identifier})')
        strings.append(self.sheetname.sexp(indent=indent+1))
        strings.append(self.filename.sexp(indent=indent+1))
        for pin in self.pins:
            strings.append(pin.sexp(indent=indent+1))
        strings.append(f'{"  " * indent})')
        return "\n".join(strings)
