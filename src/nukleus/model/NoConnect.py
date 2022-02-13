from __future__ import annotations

from dataclasses import dataclass

from .PositionalElement import PositionalElement


@dataclass
class NoConnect(PositionalElement):
    """  NoConnect schema item. """

    @classmethod
    def new(cls) -> NoConnect:
        return NoConnect('lskdfj', (0, 0), 0)

    def sexp(self, indent=1):
        return(f'{"  " * indent}(no_connect (at {self.pos[0]} {self.pos[1]}) '
               f'(uuid {self.identifier}))')
