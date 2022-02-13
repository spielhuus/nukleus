from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .PositionalElement import PositionalElement
from .TextEffects import TextEffects
from .Property import Property


@dataclass
class GlobalLabel(PositionalElement):
    text: str
    shape: str
    autoplaced: str
    text_effects: TextEffects
    properties: List[Property]

    def sexp(self, indent=1) -> str:
        strings: List[str] = []
        strings.append(f'{"  " * indent}(global_label "{self.text}" (shape {self.shape})'
                       f'(at {self.pos[0]:g} {self.pos[1]:g} {self.angle:g})'
                       f'{"" if self.autoplaced == "" else "(fields_autoplaced)"}')
        strings.append(self.text_effects.sexp(indent=indent+1))
        strings.append(f'{"  " * (indent + 1)}(uuid {self.identifier})')
        for p in self.properties:
            strings.append(p.sexp(indent=indent+1))
        # strings.append(p.sexp(indent=indent+1)
        strings.append(f'{"  " * indent})')
        print(strings)
        return "\r\n".join(strings)
