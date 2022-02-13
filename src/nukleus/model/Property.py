from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .SchemaElement import POS_T
from .TextEffects import TextEffects


@dataclass
class Property():
    key: str
    value: str
    id: str
    pos: POS_T
    angle: float
    text_effects: TextEffects|None

    # TODO id has to be incremental, maybe go to symbol
    @classmethod
    def new(cls, key: str, name: str) -> Property:
        return Property(key, name, '1', (0, 0), 0, TextEffects(0, 0, '', '', [], True))

    def sexp(self, indent=1) -> str:
        strings: List[str] = []
        print(f'?? {self.key}, {self.value} {type(self.pos[0])}, {type(self.pos[1])} {type(self.angle)}')
        strings.append(f'{"  " * indent}(property "{self.key}" "{self.value}" '
                       f'(id {self.id}) (at {self.pos[0]:g} {self.pos[1]:g} {self.angle:g})')
        if self.text_effects:
            strings.append(self.text_effects.sexp(indent=indent+1))
        strings.append(f'{"  " * indent})')
        return "\r\n".join(strings)

