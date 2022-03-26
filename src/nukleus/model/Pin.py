from __future__ import annotations

import math
from typing import Dict, List, Tuple, cast

import numpy as np

from ..SexpParser import SEXP_T
from .SchemaElement import POS_T
from .PositionalElement import PositionalElement
from .TextEffects import TextEffects


class Pin():
    """
    The pin token defines a pin in a symbol definition.
    """
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
        """Parse the sexp input.

        :param sexp SEXP_T: Sexp as List.
        :rtype Pin: The Pin Object.
        """
        _type = ''
        _style = ''
        _pos = (0, 0)
        _angle = 0
        _length = 0
        _hidden = False
        _name = ()
        _number = ()

        for token in sexp[1:]:
            if token[0] == 'at':
                _pos = (float(token[1]), float(token[2]))
                if len(token) == 4:
                    _angle = float(token[3])
            elif token[0] == 'length':
                _length = float(token[1])
            elif token[0] == 'name':
                _name = (token[1], TextEffects.parse(cast(SEXP_T, token[2])))
            elif token[0] == 'number':
                _number = (token[1], TextEffects.parse(cast(SEXP_T, token[2])))
            elif token == 'hide':
                _hidden = True
            elif token in ('input','output','bidirectional','tri_state',
                              'passive','free','unspecified','power_in','power_out',
                              'open_collector','open_emitter','no_connect'):
                _type = token
            elif token in ('line','inverted','clock','inverted_clock','input_low',
                              'clock_low','output_low','edge_clock_high','non_logic'):
                _style = token
            else:
                raise ValueError(f"unknown Pin element {token}")

        return Pin(type=_type, style=_style, pos=_pos, angle=_angle,
                   length=_length, hidden=_hidden, name=_name, number=_number)

#    def _pos(self) -> POS_T:
#        theta = np.deg2rad(self.angle)
#        rot = np.array([math.cos(theta), math.sin(theta)])
#        verts = np.array([self.pos, self.pos + rot * self.length])
#        verts = np.round(verts, 3)
#        return verts

    def calc_pos(self, pos: POS_T, offset: float=0) -> POS_T:
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

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, PinImpl):
            return False
        other_pin = cast(PinImpl, __o)
        return(self.parent.identifier == other_pin.parent.identifier and
               self.number == other_pin.number)

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
        assert key in self.dict, f'key not in PinList: {key} {self.dict.keys()}'
        return self.dict[key]
