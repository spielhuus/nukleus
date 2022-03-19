from __future__ import annotations

from typing import List

from .SchemaElement import POS_T
from .PositionalElement import PositionalElement, ffmt
from .rgb import rgb
from ..SexpParser import SEXP_T


class Junction(PositionalElement):
    """
    The junction token defines a junction in the schematic. The junction
    section will not exist if there are no junctions in the schematic.
    """
    def __init__(self, **kwargs) -> None:
        self.diameter = kwargs.get('diameter', 0)
        """he diameter token attribute defines the DIAMETER of the junction.
        A diameter of 0 is the default diameter in the system settings."""
        self.color = kwargs.get('color', rgb(0, 0, 0, 0))
        """The color token attributes define the Red, Green, Blue, and Alpha
        transparency of the junction. If all four attributes are 0, the
        default junction color is used."""
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
            if token[0] == 'at':
                _pos = (float(token[1]), float(token[2]))
                if len(token) == 4:
                    _angle = float(token[3])
            elif token[0] == 'uuid':
                _identifier = token[1]
            elif token[0] == 'diameter':
                _diameter = float(token[1])
            elif token[0] == 'color':
                _color = rgb(float(token[1]), float(token[2]), float(token[3]), float(token[4]))
            else:
                raise ValueError(f"unknown Junction element {token}")

        return Junction(identifier=_identifier, pos=_pos, angle=_angle,
                        diameter=_diameter, color=_color)


    def sexp(self, indent: int=1) -> str:
        """
        Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        strings: List[str] = []
        strings.append(f'{"  " * indent}(junction (at {self.pos[0]:g} {self.pos[1]:g}) '
                       f'(diameter {self.diameter:g}) '
                       f'(color {ffmt(self.color.r)} {ffmt(self.color.g)} '
                       f'{ffmt(self.color.b)} {ffmt(self.color.a)})')
        strings.append(f'{"  " * (indent + 1)}(uuid {self.identifier})')
        strings.append(f'{"  " * indent})')
        return "\n".join(strings)
