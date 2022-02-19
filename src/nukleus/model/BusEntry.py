from __future__ import annotations
from typing import List
from dataclasses import dataclass

import uuid

from .PositionalElement import POS_T, PositionalElement
from .StrokeDefinition import StrokeDefinition


@dataclass
class BusEntry(PositionalElement):
    """
    The bus_entry token defines a bus entry in the schematic.
    The bus entry section will not exist if there are no bus
    entries in the schematic.
    """
    size: POS_T
    stroke_definition: StrokeDefinition

    @classmethod
    def new(cls) -> BusEntry:
        """
        Create a new BusEntry instance

        Returns: BusEntry
        """
        return BusEntry(str(uuid.uuid4()), (0, 0), 0, (0, 0), StrokeDefinition())

    def sexp(self, indent: int = 1) -> str:
        """
        Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        strings: List[str] = []
        strings.append(f'{"  " * indent}(bus_entry (at {self.pos[0]} {self.pos[1]})' \
                       f' (size {self.size[0]} {self.size[1]})')
        strings.append(self.stroke_definition.sexp(indent=indent+1))
        strings.append(f'{"  " * (indent+1)}(uuid {self.identifier})')
        strings.append(f'{"  " * indent})')
        return "\n".join(strings)
