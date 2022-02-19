from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

import uuid

from .SchemaElement import SchemaElement
from .StrokeDefinition import StrokeDefinition


@dataclass
class GraphicalLine(SchemaElement):
    """
    The polyline token defines one or more lines that may or may not represent
    a polygon. This section will not exist if there are no lines in the schematic.
    """
    pts: List[Tuple[float, float]]
    stroke_definition: StrokeDefinition

    @classmethod
    def new(cls) -> GraphicalLine:
        """
        Create a new GraphicalLine object.
        """
        return GraphicalLine(str(uuid.uuid4()), [(0, 0), (0, 0)], StrokeDefinition())

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
        return "\n".join(strings)
