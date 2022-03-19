from __future__ import annotations

from typing import Dict, List, Tuple, TypeAlias, cast

import math
from copy import copy
from enum import Enum
import re
from collections import deque

import numpy as np

from ..SexpParser import SEXP_T
from .LibrarySymbol import LibrarySymbol
from .Pin import Pin, PinList
from .PositionalElement import PositionalElement
from .Property import Property
from .SchemaElement import POS_T, SchemaElement
from .TextEffects import Justify, TextEffects
from .GraphicItem import f_coord
from .Utils import ffmt


def isUnit(symbol: LibrarySymbol, unit: int) -> bool:
    match = re.match(r".*_(\d+)_\d+", symbol.identifier)
    if match:
        _unit = int(match.group(1))
        return _unit in (0, unit)
    return False

def getSymbolSize(symbol):
    sizes = []
    for unit in symbol.library_symbol.units:
        if isUnit(unit, symbol.unit):
            for graph in unit.graphics:
                sizes.append(graph.size())
            for pin in unit.pins:
                sizes.append(pin._pos())

    if len(sizes) == 0:
        return np.array([[0, 0], [0, 0]])
    return f_coord(np.array(sizes))

def pinPosition(symbol) -> List[int]: 
    res = deque([0, 0, 0, 0])

    for pin in symbol.getPins():
        assert pin.angle <= 270, "pin angle greater then 270°"
        res[int(pin.angle / 90)] += 1

    if 'x' in symbol.mirror:
        pos0 = res[0]
        pos2 = res[2]
        res[0] = pos2
        res[2] = pos0

    if 'y' in symbol.mirror:
        pos1 = res[1]
        pos3 = res[3]
        res[1] = pos1
        res[3] = pos3

    res.rotate(int(symbol.angle/90))
    return list(res)

def placeFields(symbol) -> None:
    positions = pinPosition(symbol)
    vis_fields = [x for x in symbol.properties if x.text_effects.hidden == False]
    symbol_size = f_coord(symbol._pos(getSymbolSize(symbol)))
    if len(symbol.getPins()) == 1:
        if positions[0] == 1:
            print("single pin, fields right")

        elif positions[1] == 1:
            vis_fields[0].pos = (symbol.pos[0], symbol_size[0][1]-0.762)
            assert vis_fields[0].text_effects, "pin has no text_effects"
            vis_fields[0].text_effects.justify = [Justify.CENTER]

        elif positions[2] == 1:
            print("single pin, fields left")
            vis_fields[0].pos = (0, 2.54)
            assert vis_fields[0].text_effects, "pin has no text_effects"
            vis_fields[0].text_effects.justify = [Justify.CENTER]

        elif positions[3] == 1:
            vis_fields[0].pos = (symbol.pos[0], symbol_size[1][1]+0.762)
            assert vis_fields[0].text_effects, "pin has no text_effects"
            vis_fields[0].text_effects.justify = [Justify.CENTER]
    else:
        if positions[1] == 0:
            top_pos = symbol_size[0][1] - ((len(vis_fields)-1) * 2) - 0.762
            for pin in vis_fields:
                pin.pos = (symbol.pos[0], top_pos)
                assert pin.text_effects, "pin has no text_effects"
                pin.text_effects.justify = [Justify.CENTER]
                top_pos += 2

        elif positions[0] == 0:
            top_pos = symbol_size[0][1] + \
                ((symbol_size[1][1] - symbol_size[0][1]) / 2) - \
                ((len(vis_fields)-1) * 2) / 2
            for pin in vis_fields:
                pin.pos = (symbol_size[1][0]+0.762, top_pos)
                assert pin.text_effects, "pin has no text_effects"
                pin.text_effects.justify = [Justify.LEFT]
                top_pos += 2

        elif positions[2] == 0:
            print("fields bottom")
            assert False, "implement"
        elif positions[3] == 0:
            print("fields left")
            assert False, "implement"
        else:
            print("all sides have pins")
            assert False, "implement"


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
    """Symbol Object.
       The Symbol Object represents an instance of a LibrarySymbol.
    """
    mirror: str
    library_identifier: str
    unit: int
    in_bom: bool
    on_board: bool
    on_schema: bool
    properties: List[Property]
    pins: List[PinRef]
    library_symbol: LibrarySymbol

    def __init__(self, **kwargs) -> None:
        self.mirror: str = kwargs.get('mirror', '')
        self.library_identifier: str = kwargs.get('library_identifier', '')
        self.unit: int = kwargs.get('unit', 0)
        self.in_bom: bool = kwargs.get('in_bom', True)
        self.on_board: bool = kwargs.get('on_board', True)
        self.on_schema: bool = kwargs.get('on_schema', True)
        self.properties: List[Property] = kwargs.get('properties', [])
        self.pins: List[PinRef] = kwargs.get('pins', [])
        self.library_symbol: LibrarySymbol = kwargs.get('library_symbol', None)
        super().__init__(kwargs.get('identifier', None),
                         kwargs.get('pos', (0, 0)),
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
                    _properties.append(Property.parse(cast(SEXP_T, token)))
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
    def new(cls, ref: str, lib_name: str, library_symbol: LibrarySymbol, unit: int = 0) -> Symbol:
        """
        Create a new Symbol.
        The new symbol unit is created from the library symbol.
        The lib_name overwrites the library_name.

        :param ref str: Reference of the Symbol.
        :param lib_name str: Library name.
        :param library_symbol LibrarySymbol: Library Symbol
        :param unit int: Unit number
        :rtype Symbol: New symbol instance.
        """
        assert library_symbol, "library symbol not set"
        pins = []
        properties = []
        for prop in library_symbol.properties:
            if not prop.key.startswith('ki_'):
                sym_property = copy(prop)
                if prop.key == 'Reference':
                    sym_property.value = ref
                properties.append(sym_property)

        for sub in library_symbol.units:
            _, lib_unit, _ = sub.identifier.split('_')
            if lib_unit == '0' or lib_unit == str(unit):
                for pin in sub.pins:
                    pins.append(PinRef(pin.number[0], "uuid"))

        sym = Symbol(library_identifier=lib_name, unit=unit,
                     properties=properties,
                     pins=pins, library_symbol=library_symbol)
        return sym

    def sexp(self, indent=1):
        """
        Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        strings: List[str] = []
        symbol = f'{"  " * indent}(symbol (lib_id "{self.library_identifier}")'
        symbol += f' (at {self.pos[0]} {self.pos[1]} {ffmt(self.angle)})'
        symbol += '' if self.mirror == '' else f' (mirror {self.mirror})'
        symbol += '' if self.unit == 0 else f' (unit {self.unit})'
        strings.append(symbol)
        symbol = f'{"  " * (indent + 1)}(in_bom {"yes" if self.in_bom else "no"}) '
        symbol += f'(on_board {"yes" if self.on_board else "no"})'
        strings.append(symbol)
        strings.append(f'{"  " * (indent + 1)}(uuid {self.identifier})')
        for prop in self.properties:
            strings.append(prop.sexp(indent=indent+1))

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

        # when the key is zero we want the first elemement
        # for elements with more then one units, get the first
        if key == 0:
            for item in self:
                if cast(Symbol, item).unit == 1:
                    return item
        raise Exception("key not found", key)
