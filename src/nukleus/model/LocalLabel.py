from __future__ import annotations

from dataclasses import dataclass
from typing import List
from uuid import uuid4

from .PositionalElement import PositionalElement
from .TextEffects import TextEffects


@dataclass
class LocalLabel(PositionalElement):
    """
    The label token defines an wire or bus label name in a schematic.
    """
    text: str
    text_effects: TextEffects

    @classmethod
    def new(cls) -> LocalLabel:
        """ Create a new LocalLabel instance

        Returns: LocalLabel

        """
        return LocalLabel(str(uuid4()), (0, 0), 0, "", TextEffects.new())

    def sexp(self, indent=1) -> str:
        """
        Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        strings: List[str] = []
        strings.append(
            f'{"  " * indent}(label "{self.text}" '
            '(at {self.pos[0]:g} {self.pos[1]:g} {self.angle:g})')
        strings.append(self.text_effects.sexp(indent=indent+1))
        strings.append(f'{"  " * (indent + 1)}(uuid {self.identifier})')
        strings.append(f'{"  " * indent})')
        return "\r\n".join(strings)
