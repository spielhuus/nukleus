from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Tuple, TypeAlias, cast

import numpy as np

from .LibrarySymbol import LibrarySymbol
from .SchemaElement import SchemaElement
from .Pin import Pin, PinList
from .PositionalElement import PositionalElement
from .Property import Property


MIRROR = {
    '': np.array((1, 0, 0, -1)),
    'x': np.array((1, 0, 0, 1)),
    'y': np.array((-1, 0, 0, -1)),
    # 3: np.array((0, -1)),
}


@dataclass
class PinRef():
    number: str
    uuid: str

    def sexp(self, indent=1) -> str:
        return f'{"  " * indent}(pin "{self.number}" (uuid {self.uuid}))'


@dataclass
class Symbol(PositionalElement):
    mirror: str
    library_identifier: str
    unit: int
    in_bom: bool
    on_board: bool
    properties: List[Property]
    pins: List[PinRef]
    library_symbol: LibrarySymbol | None = None

    def _pos(self, path):
        print(f'_pos : {path}')
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
        strings: List[str] = []
        symbol = f'{"  " * indent}(symbol (lib_id "{self.library_identifier})"'
        print(f'---AT: {self.property("Reference").value} {self.pos[0]}, {self.pos[1]}')
        symbol += f' (at {self.pos[0]:g} {self.pos[1]:g} {self.angle:g})'
        symbol += f' (unit {self.unit})'
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
        return "\r\n".join(strings)


class ElementList(List[SchemaElement]):
    def __init__(self):
        super().__init__(self)

    def __getitem__(self, key):
        for item in self:
            if cast(Symbol, item).unit == key:
                return item

        raise Exception("key not found", key)
