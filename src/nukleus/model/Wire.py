from __future__ import annotations

from typing import List, cast

from nukleus.model.StrokeDefinition import StrokeDefinition

from ..SexpParser import SEXP_T
from .SchemaElement import PTS_T, SchemaElement


class Wire(SchemaElement):
    """
    The wire tokens define wires in the schematic. This section will not
    exist if there are no wires in the schematic.
    """
    def __init__(self, **kwargs) -> None:
        self.pts = kwargs.get('pts', [(0, 0), (0, 0)])
        """The COORDINATE_POINT_LIST defines the list of X and Y
        coordinates of start and end points of the wire."""
        self.stroke_definition = kwargs.get(
            'stroke_definition', StrokeDefinition())
        """The STROKE_DEFINITION defines how the wire or bus is drawn."""
        super().__init__(identifier=kwargs.get('identifier', None))

    @classmethod
    def parse(cls, sexp: SEXP_T) -> Wire:
        """Parse the sexp input.

        :param sexp SEXP_T: Sexp as List.
        :rtype Wire: The Wire Object.
        """
        _identifier = None
        _pts: PTS_T = []
        _stroke_definition: StrokeDefinition = StrokeDefinition()

        for token in sexp[1:]:
            if token[0] == 'uuid':
                _identifier = token[1]
            elif token[0] == 'pts':
                for _pt in token[1:]:
                    _pts.append((float(_pt[1]), float(_pt[2])))
            elif token[0] == 'stroke':
                _stroke_definition = StrokeDefinition.parse(cast(SEXP_T, token))
            else:
                raise ValueError(f"unknown Wire element {token}")

        return Wire(identifier=_identifier, pts=_pts, stroke_definition=_stroke_definition)

    def sexp(self, indent: int = 1) -> str:
        """
        Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        strings: List[str] = []
        string = ''
        string += f'{"  " * indent}(wire (pts'
        for _pt in self.pts:
            string += f' (xy {_pt[0]:g} {_pt[1]:g})'
        string += ')'
        strings.append(string)
        strings.append(self.stroke_definition.sexp(indent=indent+1))
        strings.append(f'{"  " * (indent+1)}(uuid {self.identifier})')
        strings.append(f'{"  " * indent})')
        return "\n".join(strings)
