from __future__ import annotations

from dataclasses import dataclass

from .PositionalElement import PositionalElement


@dataclass
class NoConnect(PositionalElement):
    """
    The no_connect token defines a unused pin connection in the schematic.
    The no connect section will not exist if there are not any no connect
    in the schematic.
    """

    @classmethod
    def new(cls) -> NoConnect:
        return NoConnect('lskdfj', (0, 0), 0)

    def sexp(self, indent=1):
        """
        Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        return(f'{"  " * indent}(no_connect (at {self.pos[0]} {self.pos[1]}) '
               f'(uuid {self.identifier}))')
