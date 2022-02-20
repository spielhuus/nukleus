from __future__ import annotations

from typing import List

from ..SexpParser import SEXP_T
from .GraphicItem import GraphicItem, Polyline, Rectangle, Circle, Arc
from .Pin import Pin
from .Property import Property
from .SchemaElement import SchemaElement


class LibrarySymbol(SchemaElement):
    """
    The symbol token defines a symbol or sub-unit of a parent symbol.
    There can be zero or more symbol tokens in a symbol library.
    """
    identifier: str
    extends: str
    pin_numbers_hide: bool
    pin_names_offset: float
    pin_names_hide: bool
    in_bom: bool
    on_board: bool
    properties: List[Property]
    graphics: List[GraphicItem]
    pins: List[Pin]
    units: List[LibrarySymbol]

    def __init__(self, **kwargs) -> None:
        self.identifier: str = kwargs.get('identifier', '')
        self.extends: str = kwargs.get('extends', '')
        self.pin_numbers_hide: bool = kwargs.get('pin_numbers_hide', True)
        self.pin_names_offset: float = kwargs.get('pin_names_offset', 0)
        self.pin_names_hide: bool = kwargs.get('pin_names_hide', True)
        self.in_bom: bool = kwargs.get('in_bom', True)
        self.on_board: bool = kwargs.get('on_board', True)
        self.properties: List[Property] = kwargs.get('properties', [])
        self.graphics: List[GraphicItem] = kwargs.get('graphics', [])
        self.pins: List[Pin] = kwargs.get('pins', [])
        self.units: List[LibrarySymbol] = kwargs.get('units', [])
        super().__init__(kwargs.get('identifier', None))

    @classmethod
    def parse(cls, sexp: SEXP_T) -> LibrarySymbol:
        _identifier: str = sexp[1]
        _extends: str = ''
        _pin_numbers_hide: bool = False
        _pin_names_offset: float = 0
        _pin_names_hide: bool = True
        _in_bom: bool = True
        _on_board: bool = True
        _properties: List[Property] = []
        _graphics: List[GraphicItem] = []
        _pins: List[Pin] = []
        _units: List[LibrarySymbol] = []

        _index = 2
        if len(sexp) >= 3 and len(sexp[2]) == 1:
            _extends = sexp[2][0]
            _index += 1

        for token in sexp[_index:]:
            match token:
#                case ['lib_id', id]:
#                    _identifier = id
                case ['extends', _id]:
                    _extends = _id
                case ['pin_numbers', flag]:
                    _pin_numbers_hide = (flag == 'hide')
                case ['pin_names', 'hide']:
                    _pin_names_hide = True
                case ['pin_names', ['offset', offset]]:
                    _pin_names_offset = float(offset)
                    _pin_names_hide = False
                case ['pin_names', ['offset', offset], 'hide']:
                    _pin_names_offset = float(offset)
                    _pin_names_hide = True
                case ['in_bom', flag]:
                    _in_bom = flag == "yes"
                case ['on_board', flag]:
                    _on_board = flag == "yes"
                case ['property', *_]:
                    _properties.append(Property.parse(token))
                case ['polyline', *_]:
                    _graphics.append(Polyline.parse(token))
                case ['rectangle', *_]:
                    _graphics.append(Rectangle.parse(token))
                case ['circle', *_]:
                    _graphics.append(Circle.parse(token))
                case ['arc', *_]:
                    _graphics.append(Arc.parse(token))
                case ['symbol', *_]:
                    _units.append(LibrarySymbol.parse(token))
                case ['pin', *_]:
                    pin = Pin.parse(token)
                    _pins.append(pin)
                case ['text', *_]:
                    pass
                    # TODO print(token)
                    # _graphics.append(self._rectangle(token))
                case _:
                    raise ValueError(f"unknown lib symbol element {token}")

        return LibrarySymbol(
            identifier=_identifier, extends=_extends, pin_numbers_hide=_pin_numbers_hide,
            pin_names_offset=_pin_names_offset, pin_names_hide=_pin_names_hide,
            in_bom=_in_bom, on_board=_on_board, properties=_properties,
            graphics=_graphics, pins=_pins, units=_units)

    def sexp(self, indent=1, is_subsymbol=False):
        """
        Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        strings: List[str] = []
        symbol = f'{"  " * indent}(symbol "{self.identifier}"'
        if not is_subsymbol:
            if self.extends != '':
                symbol += f' ({self.extends})'
            if self.pin_numbers_hide:
                symbol += ' (pin_numbers hide)'
            symbol += f' (pin_names (offset {self.pin_names_offset:g})'
            if self.pin_names_hide:
                symbol += ' hide'
            symbol += ') '
            symbol += f'(in_bom {"yes" if self.in_bom else "no"}) '
            symbol += f'(on_board {"yes" if self.on_board else "no"})'
        strings.append(symbol)
        for prop in self.properties:
            strings.append(prop.sexp(indent=indent+1))

        for graphic in self.graphics:
            strings.append(graphic.sexp(indent=indent+1))

        for pin in self.pins:
            strings.append(pin.sexp(indent=indent+1))

        for uit in self.units:
            strings.append(uit.sexp(indent=indent+1, is_subsymbol=True))

        strings.append(f'{"  " * indent})')
        return "\n".join(strings)
