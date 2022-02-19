from __future__ import annotations

from typing import List

from .SchemaElement import SchemaElement, POS_T
from .StrokeDefinition import StrokeDefinition
from ..SexpParser import SEXP_T


class Bus(SchemaElement):
    """
    The bus tokens define wires and buses in the schematic.
    This section will not exist if there are no buses
    in the schematic.
    """
    pts: List[POS_T]
    stroke_definition: StrokeDefinition

    def __init__(self, **kwargs) -> None:
        self.pts = kwargs.get('pts', [(0, 0), (0, 0)])
        self.stroke_definition = kwargs.get('stroke_definition', StrokeDefinition())
        super().__init__(identifier=kwargs.get('identifier', None))

    @classmethod
    def parse(cls, sexp: SEXP_T) -> Bus:
        _identifier = None
        _pts: PTS_T = []
        _stroke_definition: StrokeDefinition = StrokeDefinition()

        for token in sexp[1:]:
            match token:
                case ['uuid', identifier]:
                    _identifier = identifier
                case ['pts', *points]:
                    for _pt in points:
                        match _pt:
                            case ['xy', _x, _y]:
                                _pts.append((float(_x), float(_y)))
                case ['stroke', *stroke]:
                    _stroke_definition = StrokeDefinition.parse(stroke)
                case _:
                    raise ValueError(f"unknown bus element {token}")

        return Bus(identifier=_identifier, pts=_pts, stroke_definition=_stroke_definition)

    def sexp(self, indent: int=1) -> str:
        """
        Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        strings: List[str] = []
        string = f'{"  " * indent}(bus (pts'
        for _pt in self.pts:
            string += f' (xy {_pt[0]:g} {_pt[1]:g})'
        string += ')'
        strings.append(string)
        strings.append(self.stroke_definition.sexp(indent=indent+1))
        strings.append(f'{"  " * (indent+1)}(uuid {self.identifier})')
        strings.append(f'{"  " * indent})')
        return "\n".join(strings)
