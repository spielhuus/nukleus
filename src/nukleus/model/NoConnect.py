from __future__ import annotations

from ..SexpParser import SEXP_T
from .SchemaElement import POS_T
from .PositionalElement import PositionalElement


class NoConnect(PositionalElement):
    """
    The no_connect token defines a unused pin connection in the schematic.
    The no connect section will not exist if there are not any no connect
    in the schematic.
    """
    def __init__(self, **kwargs) -> None:
        super().__init__(kwargs.get('identifier', None),
                         kwargs.get('pos', ((0, 0), (0, 0))),
                         kwargs.get('angle', 0))

    @classmethod
    def parse(cls, sexp: SEXP_T) -> NoConnect:
        """Parse the sexp input.

        :param sexp SEXP_T: Sexp as List.
        :rtype NoConnect: The NoConnect Object.
        """
        _identifier = None
        _pos: POS_T = (0, 0)
        _angle: float = 0

        for token in sexp[1:]:
            if token[0] == 'at':
                _pos = (float(token[1]), float(token[2]))
                if len(token) == 4:
                    _angle = float(token[3])
            elif token[0] == 'uuid':
                _identifier = token[1]
            else:
                raise ValueError(f"unknown NoConnect element {token}")

        return NoConnect(identifier=_identifier, pos=_pos, angle=_angle)

    def sexp(self, indent: int = 1) -> str:
        """Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        return(f'{"  " * indent}(no_connect (at {self.pos[0]} {self.pos[1]}) '
               f'(uuid {self.identifier}))')
