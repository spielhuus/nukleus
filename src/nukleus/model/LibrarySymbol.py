from __future__ import annotations

from typing import List, cast

from ..SexpParser import SEXP_T
from .GraphicItem import Arc, Circle, GraphicItem, Polyline, Rectangle, Text
from .Pin import Pin
from .Property import Property
from .SchemaElement import SchemaElement


class LibrarySymbol(SchemaElement):
    """
    The symbol token defines a symbol or sub-unit of a parent symbol.
    There can be zero or more symbol tokens in a symbol library.
    """
    def __init__(self, **kwargs) -> None:
        self.identifier: str = kwargs.get('identifier', '')
        """Each symbol must have a unique "LIBRARY_ID" for each top level symbol
        in the library or a unique "UNIT_ID" for each unit embedded in a parent
        symbol. Library identifiers are only valid it top level symbols and unit
        identifiers are on valid as unit symbols inside a parent symbol."""
        self.extends: str = kwargs.get('extends', '')
        """The optional extends token attribute defines the "LIBRARY_ID" of another
        symbol inside the current library from which to derive a new symbol.
        Extended symbols currently can only have different SYMBOL_PROPERTIES
        than their parent symbol."""
        self.pin_numbers_hide: bool = kwargs.get('pin_numbers_hide', True)
        """The optional pin_numbers token defines the visibility setting of
        the symbol pin numbers for the entire symbol. If not defined, the
        all of the pin numbers in the symbol are visible."""
        self.pin_names_offset: float = kwargs.get('pin_names_offset', 0)
        """The optional offset token defines the pin name offset for all pin
        names of the symbol. If not defined, the pin name offset is 0.508mm (0.020")."""
        self.pin_names_hide: bool = kwargs.get('pin_names_hide', True)
        """The optional pin_names token defines the visibility for all of the
        pin names of the symbol"""
        self.in_bom: bool = kwargs.get('in_bom', True)
        """The in_bom token, defines if a symbol is to be include in the
        bill of material output. The only valid attributes are yes and no."""
        self.on_board: bool = kwargs.get('on_board', True)
        """The on_board token, defines if a symbol is to be exported from the
        schematic to the printed circuit board. The only valid attributes are yes and no."""
        self.properties: List[Property] = kwargs.get('properties', [])
        """The SYMBOL_PROPERTIES is a list of properties that define the symbol.
        The following properties are mandatory when defining a parent symbol:
            -"Reference",
            -"Value",
            -"Footprint",
            -"Datasheet".
        All other properties are optional. Unit symbols cannot have any properties."""
        self.graphics: List[GraphicItem] = kwargs.get('graphics', [])
        """The GRAPHIC ITEMS section is list of graphical arcs, circles, curves, lines,
        polygons, rectangles and text that define the symbol drawing.
        This section can be empty if the symbol has no graphical items."""
        self.pins: List[Pin] = kwargs.get('pins', [])
        """The PINS section is a list of pins that are used by the symbol.
        This section can be empty if the symbol does not have any pins."""
        self.units: List[LibrarySymbol] = kwargs.get('units', [])
        """The optional UNITS can be one or more child symbol tokens
        embedded in a parent symbol."""
        super().__init__(kwargs.get('identifier', None))

    @classmethod
    def parse(cls, sexp: SEXP_T) -> LibrarySymbol:
        """Parse the sexp input.

        :param sexp SEXP_T: Sexp as List.
        :rtype LibrarySymbol: The LibrarySymbol Object.
        """
        _identifier: str = cast(str, sexp[1])
        _extends: str = ''
        _pin_numbers_hide: bool = False
        _pin_names_offset: float = 0
        _pin_names_hide: bool = False
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
            if token[0] == 'extends':
                _extends = token[1]
            elif token[0] == 'pin_numbers':
                _pin_numbers_hide = (token[1] == 'hide')
            elif token[0] == 'pin_names' and token[1] == 'hide':
                _pin_names_hide = True
            elif token[0] == 'pin_names' and token[1][0] == 'offset':
                _pin_names_offset = float(token[1][1])
                if len(token) == 3 and token[2] == 'hide':
                    _pin_names_hide = True
            elif token[0] == 'in_bom':
                _in_bom = (token[1] == 'yes')
            elif token[0] == 'on_board':
                _on_board = (token[1] == 'yes')
            elif token[0] == 'property':
                _properties.append(Property.parse(cast(SEXP_T, token)))
            elif token[0] == 'polyline':
                _graphics.append(Polyline.parse(cast(SEXP_T, token)))
            elif token[0] == 'rectangle':
                _graphics.append(Rectangle.parse(cast(SEXP_T, token)))
            elif token[0] == 'circle':
                _graphics.append(Circle.parse(cast(SEXP_T, token)))
            elif token[0] == 'arc':
                _graphics.append(Arc.parse(cast(SEXP_T, token)))
            elif token[0] == 'symbol':
                _units.append(LibrarySymbol.parse(cast(SEXP_T, token)))
            elif token[0] == 'pin':
                pin = Pin.parse(cast(SEXP_T, token))
                _pins.append(pin)
            elif token[0] == 'text':
                _graphics.append(Text.parse(cast(SEXP_T, token)))
            else:
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
