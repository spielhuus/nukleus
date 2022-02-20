from __future__ import annotations

import math
from enum import Enum
from typing import Dict, List, Tuple, TypeAlias, cast

import numpy as np

from ..SexpParser import SEXP_T
from .LibrarySymbol import LibrarySymbol
from .Pin import Pin, PinList
from .PositionalElement import PositionalElement
from .Property import Property
from .SchemaElement import POS_T, SchemaElement

MIRROR = {
    '': np.array((1, 0, 0, -1)),
    'x': np.array((1, 0, 0, 1)),
    'y': np.array((-1, 0, 0, -1)),
    # 3: np.array((0, -1)),
}


class PinRef():
    number: str
    uuid: str

    def __init__(self, number, identifier) -> None:
        self.number: str = number
        self.identifier: str = identifier

    def sexp(self, indent=1) -> str:
        return f'{"  " * indent}(pin "{self.number}" (uuid {self.identifier}))'


class Symbol(PositionalElement):
    mirror: str
    library_identifier: str
    unit: int
    in_bom: bool
    on_board: bool
    properties: List[Property]
    pins: List[PinRef]
    library_symbol: LibrarySymbol

    def __init__(self, **kwargs) -> None:
        self.mirror: str = kwargs.get('mirror', '')
        self.library_identifier: str = kwargs.get('library_identifier', '')
        self.unit: int = kwargs.get('unit', 0)
        self.in_bom: bool = kwargs.get('in_bom', True)
        self.on_board: bool = kwargs.get('on_board', True)
        self.properties: List[Property] = kwargs.get('properties', [])
        self.pins: List[PinRef] = kwargs.get('pins', [])
        self.library_symbol: LibrarySymbol = kwargs.get('library_symbol', None)
        super().__init__(kwargs.get('identifier', None),
                         kwargs.get('pos', ((0, 0), (0, 0))),
                         kwargs.get('angle', 0))

    @classmethod
    def parse(cls, sexp: SEXP_T) -> Symbol:
        _identifier: str = ''
        _pos: POS_T = (0, 0)
        _angle: float = 0
        _mirror: str = ''
        _library_identifier: str = ''
        _unit: int = 0
        _in_bom: bool = True
        _on_board: bool = True
        _properties: List[Property] = []
        _pins: List[PinRef] = []
        _library_symbol: LibrarySymbol | None = None

        for token in sexp[1:]:
            match token:
                case ['lib_id', id]:
                    _library_identifier = id
                case ['at', x, y, angle]:
                    _pos = (float(x), float(y))
                    _angle = float(angle)
                case ['at', x, y]:
                    _pos = (float(x), float(y))
                case ['mirror', mirror]:
                    _mirror = mirror
                case ['unit', id]:
                    _unit = int(id)
                case ['in_bom', flag]:
                    _in_bom = flag == "yes"
                case ['on_board', flag]:
                    _on_board = flag == "yes"
                case ['uuid', uuid]:
                    _identifier = uuid
                case ['property', *_]:
                    _properties.append(Property.parse(token))
                case ['fields_autoplaced']:
                    pass  # TODO
                case ['pin', *items]:
                    _pins.append(PinRef(items[0], items[1][1]))
                case _:
                    raise ValueError(f"unknown symbol element {token}")

        return Symbol(identifier=_identifier, pos=_pos, angle=_angle,
                      mirror=_mirror, library_identifier=_library_identifier, unit=_unit,
                      in_bom=_in_bom, on_board=_on_board, properties=_properties,
                      pins=_pins, library_symbol=_library_symbol)

    def _pos(self, path):
        theta = np.deg2rad(self.angle)
        trans = np.reshape(MIRROR[self.mirror], (2, 2)).T
        rot = np.array([[math.cos(theta), -math.sin(theta)],
                        [math.sin(theta), math.cos(theta)]])

        verts = np.matmul(path, rot)
        verts = np.matmul(verts, trans)
        verts = (self.pos + verts)
        verts = np.round(verts, 3)
        return verts

    def property(self, name: str) -> Property:
        for property in self.properties:
            if property.key == name:
                return property
        raise LookupError("property not found:%s", name)

    def has_property(self, name: str) -> bool:
        for property in self.properties:
            if property.key == name:
                return True
        return False

    def getPins(self) -> PinList:
        _pins = PinList()
        single_unit = False
        assert self.library_symbol, 'library symbol is not set'
        for subsym in self.library_symbol.units:
            unit = int(subsym.identifier.split('_')[-2])
            single_unit = True if unit == 0 else single_unit
            if unit == 0 or unit == self.unit or single_unit:
                _pins.extend(self, subsym.pins)

        return _pins

    @classmethod
    def new(cls, ref, lib_name, library_symbol, unit: int = 0) -> Symbol:  # TODO ref must be id
        assert library_symbol, "library symbol not set"
        pins = []  # TODO
        for sub in library_symbol.units:
            for pin in sub.pins:
                pins.append(pin)
        sym = Symbol(ref, (0, 0), 0, '', lib_name, unit,
                     True, True, library_symbol.properties,
                     pins, library_symbol)
        return sym

    def sexp(self, indent=1):
        """
        Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        strings: List[str] = []
        symbol = f'{"  " * indent}(symbol (lib_id "{self.library_identifier}")'
        symbol += f' (at {self.pos[0]:4g} {self.pos[1]:4g} {self.angle:g})'
        symbol += '' if self.mirror == '' else f' (mirror {self.mirror})'
        symbol += '' if self.unit == 0 else f' (unit {self.unit})'
        strings.append(symbol)
        symbol = f'{"  " * (indent + 1)}(in_bom {"yes" if self.in_bom else "no"}) '
        symbol += f'(on_board {"yes" if self.on_board else "no"})'
        strings.append(symbol)
        strings.append(f'{"  " * (indent + 1)}(uuid {self.identifier})')
        for property in self.properties:
            strings.append(property.sexp(indent=indent+1))

        for pin in self.pins:
            strings.append(pin.sexp(indent=indent+1))

        strings.append(f'{"  " * indent})')
        return "\n".join(strings)


class ElementList(List[SchemaElement]):
    def __init__(self):
        super().__init__(self)

    def __getitem__(self, key):
        for item in self:
            if cast(Symbol, item).unit == key:
                return item

        raise Exception("key not found", key)
