from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .PositionalElement import PositionalElement


@dataclass
class Junction(PositionalElement):
    """
    The junction token defines a junction in the schematic. The junction
    section will not exist if there are no junctions in the schematic.
    """
    diameter: int
    color: str  # TODO use rgb

    @classmethod
    def new(cls) -> Junction:
        return Junction('lskdfj', (0, 0), 0, 1, "0 0 0 0")

    def sexp(self, indent=1):
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
        return "\r\n".join(strings)
