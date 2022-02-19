from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

from .SchemaElement import SchemaElement
from .StrokeDefinition import StrokeDefinition


@dataclass
class SymbolInstance(SchemaElement):
    pts: List[Tuple[float, float]]
    scale: float
    image_data: str

    @classmethod
    def new(cls) -> SymbolInstance:
        # TODO ID
        return SymbolInstance('lskdfj', [(0, 0), (0, 0)], 1, '')

    def sexp(self, indent: int=1) -> str:
        """
        Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        strings: List[str] = []
        string = ''
        string += f'{"  " * indent}(path (pts'
        print(self.pts)
        for p in self.pts:
            string += f' (xy {p[0]:g} {p[1]:g})'
        string += ')'
        strings.append(string)
        strings.append(self.stroke_definition.sexp(indent=indent+1))
        strings.append(f'{"  " * (indent+1)}(uuid {self.identifier})')
        strings.append(f'{"  " * indent})')
        return "\r\n".join(strings)
