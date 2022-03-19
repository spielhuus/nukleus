from __future__ import annotations
from typing import List, Tuple, cast

from .SchemaElement import POS_T, PTS_T
from .PositionalElement import PositionalElement
from .StrokeDefinition import StrokeDefinition
from ..SexpParser import SEXP_T

class BusEntry(PositionalElement):
    """
    The bus_entry token defines a bus entry in the schematic.
    The bus entry section will not exist if there are no bus
    entries in the schematic.
    """
    def __init__(self, **kwargs) -> None:
        self.size: PTS_T =  kwargs.get('size', (0, 0))
        """The size token attributes define the X and Y distance of
        the end point from the position of the bus entry."""
        self.stroke_definition: StrokeDefinition = \
            kwargs.get('stroke_definition', StrokeDefinition())
        """The STROKE_DEFINITION defines how the bus entry is drawn."""
        super().__init__(
            kwargs.get("identifier", None),
            kwargs.get("pos", ((0, 0), (0, 0))),
            kwargs.get("angle", 0),
        )

    @classmethod
    def parse(cls, sexp: SEXP_T) -> BusEntry:
        """Parse the sexp input.

        :param sexp SEXP_T: Sexp as List.
        :rtype BusEntry: The BusEntry Object.
        """
        _pos: POS_T = (0, 0)
        _angle: float = 0
        _size: Tuple[float, float] = (0, 0)
        _identifier = None
        _stroke_definition: StrokeDefinition = StrokeDefinition()

        for token in sexp[1:]:
            if token[0] == 'at':
                _pos = (float(token[1]), float(token[2]))
                if len(token) == 4:
                    _angle = float(token[3])
            elif token[0] == 'size':
                _size = (float(token[1]), float(token[2]))
            elif token[0] == 'uuid':
                _identifier = token[1]
            elif token[0] == 'stroke':
                _stroke_definition = StrokeDefinition.parse(cast(SEXP_T, token))
            else:
                raise ValueError(f"unknown BusEntry element {token}")

        return BusEntry(pos=_pos, angle=_angle, size=_size,
                identifier=_identifier, stroke_definition=_stroke_definition)

    def sexp(self, indent: int = 1) -> str:
        """
        Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        strings: List[str] = []
        strings.append(f'{"  " * indent}(bus_entry (at {self.pos[0]} {self.pos[1]})'
                       f' (size {self.size[0]} {self.size[1]})')
        strings.append(self.stroke_definition.sexp(indent=indent+1))
        strings.append(f'{"  " * (indent+1)}(uuid {self.identifier})')
        strings.append(f'{"  " * indent})')
        return "\n".join(strings)
