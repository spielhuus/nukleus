from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np

from .PositionalElement import POS_T, PositionalElement
from .TextEffects import TextEffects


@dataclass
class Pin():
    type: str
    style: str
    pos: POS_T
    angle: float
    length: float
    hidden: bool
    name: Tuple[str, TextEffects]
    number: Tuple[str, TextEffects]

    @classmethod
    def new(cls, number: str, name: str) -> Pin:
        return Pin("", "", (0, 0), 0, 0, True,
                   (name, TextEffects.new()),
                   (number, TextEffects.new()))

    def _pos(self):
        theta = np.deg2rad(self.angle)
        rot = np.array([math.cos(theta), math.sin(theta)])
        return np.array([self.pos, self.pos + rot * self.length])

    def sexp(self, indent=1) -> str:
        strings: List[str] = []
        strings.append(f'{"  " * indent}(pin {self.type} {self.style} (at {self.pos[0]:g} '
                       f'{self.pos[1]:g} {self.angle:g}) (length {self.length:g})'
                       f'{"" if self.hidden == False else " hide"}')
        strings.append(
            f'{"  " * (indent + 1)}(name "{self.name[0]}" {self.name[1].sexp(indent=0)})')
        strings.append(
            f'{"  " * (indent + 1)}(number "{self.number[0]}" {self.number[1].sexp(indent=0)})')
        strings.append(f'{"  " * indent})')
        return "\r\n".join(strings)


class PinImpl(Pin):
    def __init__(self, parent: PositionalElement, pin):
        super().__init__(pin.type, pin.style, pin.pos, pin.angle,
                         pin.length, pin.hidden, pin.name, pin.number)
        self.parent = parent


class PinList():
    def __init__(self):
        self.dict: Dict = {}

    def append(self, parent: PositionalElement, item: Pin):
        self.dict[item.number[0]] = PinImpl(parent, item)

    def extend(self, parent: PositionalElement, pins: List[Pin]):
        for pin in pins:
            self.dict[pin.number[0]] = PinImpl(parent, pin)

    def __iter__(self):
        ''' Returns the Iterator object '''
        return iter(self.dict.values())

    def __len__(self):
        return len(self.dict)

    def __getitem__(self, key: str):
        assert key in self.dict, f'key not in PinList: {key}'
        return self.dict[key]
