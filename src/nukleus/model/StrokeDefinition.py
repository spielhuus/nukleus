from __future__ import annotations

from dataclasses import dataclass
from typing import List


class rgb():
    def __init__(self, r: int, g: int, b: int, a: int):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def get_hex(self):
        return "#{int(r, 16)}{int(g, 16)}{int(b, 16)}{int(a*100, 16)}"

    def get(self):
        return (self.r, self.g, self.b, self.a)

    def __eq__(self, other):
        return self.r == other.r and \
            self.g == other.g and \
            self.b == other.b and \
            self.a == other.a

@dataclass
class StrokeDefinition():
    """Stroke definition of a line"""
    width: float
    type: str
    color: rgb

    @classmethod
    def new(cls) -> StrokeDefinition:
        return StrokeDefinition(0, '', rgb(0, 0, 0, 0))

    def sexp(self, indent=1):
        strings: List[str] = []
        strings.append(f'{"  " * indent}(stroke ')
        strings.append(f'(width {self.width:g}) ')
        strings.append(f'(type {self.type}) ')
        strings.append(f'(color {self.color.r} {self.color.g} '
                       f'{self.color.b} {self.color.a}))')
        return "".join(strings)
