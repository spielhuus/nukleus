from __future__ import annotations

from typing import List, cast
from copy import copy
from ..SexpParser import SEXP_T
from .LibrarySymbol import LibrarySymbol
from .Pin import PinList
from .PositionalElement import PositionalElement, ffmt
from .Property import Property
from .SchemaElement import POS_T, SchemaElement


class PinRef():
    """Sympol Pin Reference"""
    def __init__(self, number, identifier) -> None:
        self.number: str = number
        self.identifier: str = identifier

    def sexp(self, indent=1) -> str:
        return f'{"  " * indent}(pin "{self.number}" (uuid {self.identifier}))'


class Symbol(PositionalElement):
    """Symbol Object.
       The Symbol Object represents an instance of a LibrarySymbol.
    """
#    mirror: str
#    library_identifier: str
#    unit: int
#    in_bom: bool
#    on_board: bool
#    on_schema: bool
#    properties: List[Property]
#    pins: List[PinRef]
#    library_symbol: LibrarySymbol
#
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
            if token[0] == 'lib_id':
                _library_identifier = token[1]
            elif token[0] == 'at':
                _pos = (float(token[1]), float(token[2]))
                if len(token) == 4:
                    _angle = float(token[3])
            elif token[0] == 'mirror':
                _mirror = token[1]
            elif token[0] == 'unit':
                _unit = int(token[1])
            elif token[0] == 'in_bom':
                _in_bom = token[1] == "yes"
            elif token[0] == 'on_board':
                _on_board = token[1] == "yes"
            elif token[0] == 'uuid':
                _identifier = token[1]
            elif token[0] == 'property':
                _properties.append(Property.parse(cast(SEXP_T, token)))
            elif token[0] == 'fields_autoplaced':
                pass  # TODO
            elif token[0] == 'pin':
                _pins.append(PinRef(token[1], token[2][1]))
            else:
                raise ValueError(f"unknown symbol element {token}")

        return Symbol(identifier=_identifier, pos=_pos, angle=_angle,
                      mirror=_mirror, library_identifier=_library_identifier, unit=_unit,
                      in_bom=_in_bom, on_board=_on_board, properties=_properties,
                      pins=_pins, library_symbol=_library_symbol)

    def property(self, name: str) -> Property:
        """
        Get Property by key.

        :param name str: The Property Key.
        :rtype Property: The Property.
        :raises LookupError: When the property does not exist.
        """
        for prop in self.properties:
            if prop.key == name:
                return prop
        raise LookupError(f"property not found: {name}")

    def has_property(self, name: str) -> bool:
        """
        Test if the Sybol has property by key.

        :param name str: The Property Key.
        :rtype bool: True if the Property exists.
        """
        for prop in self.properties:
            if prop.key == name:
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
