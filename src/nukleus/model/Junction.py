from __future__ import annotations

from typing import List

from .PositionalElement import PositionalElement, POS_T
from .rgb import rgb
from ..SexpParser import SEXP_T


class Junction(PositionalElement):
    """
    The junction token defines a junction in the schematic. The junction
    section will not exist if there are no junctions in the schematic.
    """
    diameter: int
    color: rgb

    def __init__(self, **kwargs) -> None:
        self.diameter = kwargs.get('diameter', 0)
        self.color = kwargs.get('color', rgb(0, 0, 0, 0))
        super().__init__(kwargs.get('identifier', None),
                         kwargs.get('pos', ((0, 0), (0, 0))),
                         kwargs.get('angle', 0))

    @classmethod
    def parse(cls, sexp: SEXP_T) -> Junction:
        """Parse the sexp input.

        :param sexp SEXP_T: Sexp as List.
        :rtype Polyline: The NoConnect Object.
        """
        _identifier = None
        _pos: POS_T = (0, 0)
        _angle: float = 0
        _diameter: float = 0
        _color: rgb = rgb(0, 0, 0, 0)

        for token in sexp[1:]:
            match token:
                case ['uuid', identifier]:
                    _identifier = identifier
                case ['at', _x, _y]:
                    _pos = (float(_x), float(_y))
                case ['diameter', _d]:
                    _diameter = float(_d)
                case ['color', r, g, b, a]:
                    _color = rgb(float(r), float(g), float(b), float(a))
                case _:
                    raise ValueError(f"unknown junction element {token}")

        return Junction(identifier=_identifier, pos=_pos, angle=_angle,
                        diameter=_diameter, color=_color)


    def sexp(self, indent: int=1) -> str:
        """
        Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        strings: List[str] = []
        strings.append((f'{"  " * indent}(junction (at {self.pos[0]:g} {self.pos[1]:g}) '
                        f'(diameter {self.diameter:g}) (color 0 0 0 0)'))  # TODO use rgb
        strings.append(f'{"  " * (indent + 1)}(uuid {self.identifier})')
        strings.append(f'{"  " * indent})')
        return "\n".join(strings)
