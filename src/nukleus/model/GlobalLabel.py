from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .PositionalElement import PositionalElement
from .Property import Property
from .TextEffects import TextEffects


@dataclass
class GlobalLabel(PositionalElement):
    """ The global_label token defines a label name that is visible across all
        schematics in a design. This section will not exist if no global labels
        are defined in the schematic.
    """
    text: str
    shape: str
    autoplaced: str
    text_effects: TextEffects
    properties: List[Property]

    def sexp(self, indent=1) -> str:
        """
        Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        strings: List[str] = []
        strings.append(f'{"  " * indent}(global_label "{self.text}" (shape {self.shape})'
                       f'(at {self.pos[0]:g} {self.pos[1]:g} {self.angle:g})'
                       f'{"" if self.autoplaced == "" else "(fields_autoplaced)"}')
        strings.append(self.text_effects.sexp(indent=indent+1))
        strings.append(f'{"  " * (indent + 1)}(uuid {self.identifier})')
        for prop in self.properties:
            strings.append(prop.sexp(indent=indent+1))
        strings.append(f'{"  " * indent})')
        print(strings)
        return "\r\n".join(strings)
