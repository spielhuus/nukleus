from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .PositionalElement import PositionalElement


@dataclass
class Junction(PositionalElement):
    diameter: int
    color: str  # TODO use rgb

    @classmethod
    def new(cls) -> Junction:
        return Junction('lskdfj', (0, 0), 0, 1, "0 0 0 0")

    def sexp(self, indent=1):
        strings: List[str] = []
        strings.append((f'{"  " * indent}(junction (at {self.pos[0]:g} {self.pos[1]:g}) '
                        f'(diameter {self.diameter:g}) (color 0 0 0 0)'))  # TODO use rgb
        strings.append(f'{"  " * (indent + 1)}(uuid {self.identifier})')
        strings.append(f'{"  " * indent})')
        return "\r\n".join(strings)
