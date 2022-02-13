from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

from .SchemaElement import SchemaElement
from .StrokeDefinition import StrokeDefinition


@dataclass
class Wire(SchemaElement):
    pts: List[Tuple[float, float]]
    stroke_definition: StrokeDefinition

    @classmethod
    def new(cls) -> Wire:
        # TODO ID
        return Wire('lskdfj', [(0, 0), (0, 0)], StrokeDefinition.new())

    def sexp(self, indent=1):
        strings: List[str] = []
        string = ''
        string += f'{"  " * indent}(wire (pts'
        print(self.pts)
        for p in self.pts:
            string += f' (xy {p[0]:g} {p[1]:g})'
        string += ')'
        strings.append(string)
        strings.append(self.stroke_definition.sexp(indent=indent+1))
        strings.append(f'{"  " * (indent+1)}(uuid {self.identifier})')
        strings.append(f'{"  " * indent})')
        return "\r\n".join(strings)
