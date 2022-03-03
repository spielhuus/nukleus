from __future__ import annotations

import math
from typing import Any, Dict, List, Tuple, cast

import numpy as np

from ..SexpParser import SEXP_T
from .PositionalElement import POS_T, PositionalElement
from .TextEffects import TextEffects


class Pin():
    """
    The pin token defines a pin in a symbol definition.
    """
    type: str
    style: str
    pos: POS_T
    angle: float
    length: float
    name: Tuple[str, TextEffects]
    number: Tuple[str, TextEffects]

    def __init__(self, **kwargs) -> None:
        self.type = kwargs.get('type', '')
        self.style = kwargs.get('style', '')
        self.pos = kwargs.get('pos', (0, 0))
        self.angle = kwargs.get('angle', 0)
        self.hidden = kwargs.get('hidden', False)
        self.length = kwargs.get('length', 0)
        self.name = kwargs.get('name', ('~', TextEffects()))
        self.number = kwargs.get('number', ('0', TextEffects()))

    @classmethod
    def parse(cls, sexp: SEXP_T) -> Pin:
        _type = ''
        _style = ''
        _pos = (0, 0)
        _angle = 0
        _length = 0
        _hidden = False
        _name = ()
        _number = ()

        for token in sexp[1:]:
            match token:
                case ['at', x, y, angle]:
                    _pos = (float(x), float(y))
                    _angle = float(angle)
                case ['at', x, y]:
                    _pos = (float(x), float(y))
                case ['length', length]:
                    _length = float(length)
                case ['name', name, *effects]:
                    _name = (name, TextEffects.parse(cast(SEXP_T, effects[0])))
                case ['number', number, *effects]:
                    _number = (number, TextEffects.parse(cast(SEXP_T, effects[0])))
                case 'hide':
                    _hidden = True
                case 'input'|'output'|'bidirectional'|'tri_state'|'passive'|'free'|'unspecified'| \
                     'power_in'|'power_out'|'open_collector'|'open_emitter'|'no_connect':
                    _type = token
                case 'line'|'inverted'|'clock'|'inverted_clock'|'input_low'|'clock_low'| \
                     'output_low'|'edge_clock_high'|'non_logic':
                    _style = token
                case _:
                    raise ValueError(f"unknown property element {token}")


        return Pin(type=_type, style=_style, pos=_pos, angle=_angle,
                   length=_length, hidden=_hidden, name=_name, number=_number)

    def _pos(self) -> POS_T:
        theta = np.deg2rad(self.angle)
        rot = np.array([math.cos(theta), math.sin(theta)])
        verts = np.array([self.pos, self.pos + rot * self.length])
        verts = np.round(verts, 3)
        return verts

    def calc_pos(self, pos: POS_T, offset=0) -> POS_T:
        theta = np.deg2rad(self.angle)
        rot = np.array([math.cos(theta), math.sin(theta)])
        verts = np.array([pos, pos + rot * self.length + offset])
        verts = np.round(verts, 3)
        return verts

    def sexp(self, indent=1) -> str:
        """
        Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        strings: List[str] = []
        string = f'{"  " * indent}(pin {self.type} {self.style} (at {self.pos[0]:g} '
        string += f'{self.pos[1]:g} {self.angle:g}) (length {self.length:g})'
        if self.hidden:
            string += ' hide'
        strings.append(string)
        strings.append(
            f'{"  " * (indent + 1)}(name "{self.name[0]}" {self.name[1].sexp(indent=0)})')
        strings.append(
            f'{"  " * (indent + 1)}(number "{self.number[0]}" {self.number[1].sexp(indent=0)})')
        strings.append(f'{"  " * indent})')
        return "\n".join(strings)


class PinImpl(Pin):
    def __init__(self, parent: PositionalElement, pin: Pin):
        super().__init__(type=pin.type, style=pin.style, pos=pin.pos, angle=pin.angle,
                         length=pin.length, hidden=pin.hidden, name=pin.name, number=pin.number)
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
