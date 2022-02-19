from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

import uuid

from .SchemaElement import SchemaElement
from .StrokeDefinition import StrokeDefinition


@dataclass
class GraphicalText(SchemaElement):
    """
    The text token defines graphical text in a schematic.
    """
    pts: List[Tuple[float, float]]
    stroke_definition: StrokeDefinition

    @classmethod
    def new(cls) -> GraphicalText:
        """
        Create a new GlobalLabel object.
        """
        return GraphicalText(str(uuid.uuid4()), [(0, 0), (0, 0)], StrokeDefinition.new())

    def sexp(self, indent: int=1) -> str:
        """
        Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        strings: List[str] = []
        string = ''
        string += f'{"  " * indent}(polyline (pts'
        print(self.pts)
        for _pt in self.pts:
            string += f' (xy {_pt[0]:g} {_pt[1]:g})'
        string += ')'
        strings.append(string)
        strings.append(self.stroke_definition.sexp(indent=indent+1))
        strings.append(f'{"  " * (indent+1)}(uuid {self.identifier})')
        strings.append(f'{"  " * indent})')
        return "\r\n".join(strings)
