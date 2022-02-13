from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .SchemaElement import SchemaElement
from .Property import Property
from .GraphicItem import GraphicItem
from .Pin import Pin


@dataclass
class LibrarySymbol(SchemaElement):
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

    @classmethod
    def new(cls):
        return LibrarySymbol('', '', True, 0, True, False, False, [], [], [], [])

    def sexp(self, indent=1, is_subsymbol=False):
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

        for u in self.units:
            strings.append(u.sexp(indent=indent+1, is_subsymbol=True))

        strings.append(f'{"  " * indent})')
        return "\r\n".join(strings)
