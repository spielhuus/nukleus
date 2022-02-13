from typing import Optional, Tuple, cast

from nukleus import Library
from nukleus.model import Symbol, LibrarySymbol, Pin, PositionalElement, Property, POS_T

from .DrawElement import DrawElement, PinNotFoundError, totuple


class Element(DrawElement):
    def __init__(self, ref, lib_name, value=None, unit=1, **kwargs):
        self.ref = ref
        self.lib_name = lib_name
        self._value = value
        self.unit = unit
        self.properties = kwargs

        self.pos = None
        self._anchor: str = '0'
        self._angle = 0
        self.library_symbol: Optional[LibrarySymbol] = None
        self.element: Optional[Symbol] = None

    def _pin(self, number: int | str) -> Pin:
        _number = number if isinstance(number, str) else str(number)
        assert self.library_symbol is not None
        for subsym in self.library_symbol.units:
            for _pin in subsym.pins:
                if _pin.number[0] == _number:
                    return _pin

        raise PinNotFoundError("pin not found in symbol", number,
                               cast(Symbol, self.element).property("Reference").value)

    def pin(self, number: int) -> POS_T:
        assert self.element is not None
        return self.element._pos(self._pin(number)._pos())[0]

    def _get(self, library: Library, last_pos: POS_T, _: float):
        self.library_symbol = library.get(self.lib_name)
        self.library_symbol.identifier = self.lib_name
        self.element = Symbol.new(self.ref, self.lib_name, self.library_symbol)
        self.element.unit = self.unit
        self.element.angle = self._angle
        self.element.property("Reference").value = self.ref
        if self._value:
            self.element.property("Value").value = self._value

        for name, value in self.properties.items():
            if self.element.has_property(name):
                self.element.property(name).value = value
            else:
                new_property = Property.new(name, value)
                # TODO new_property.pos = tuple(totuple(self.element._pos(new.pos)))
                self.element.properties.append(new_property)

        if self.lib_name == "Device:R":
            if not self.element.has_property('Spice_Netlist_Enabled'):
                self.element.properties.append(Property.new('Spice_Netlist_Enabled', 'Y'))
            if not self.element.has_property('Spice_Primitive'):
                self.element.properties.append(Property.new('Spice_Primitive', 'R'))

        # get the anchor pins
        pins = self.element.getPins()
        _pin_numbers = [x.number[0] for x in pins]
        if self._anchor == '0' and len(pins) > 0:
            self._anchor = _pin_numbers[-1]

        # calculate position
        _pos = self.pos if self.pos is not None else last_pos
        self.element.pos = tuple(totuple(_pos -
                   self.element._pos(pins[self._anchor]._pos())[0]))

        # when the anchor pin in found, set the next pos
        if self._anchor != '0':
            _last_pos = tuple(totuple(self.element._pos(self._pin(_pin_numbers[0])._pos())[0]))
        else:
            _last_pos = tuple(totuple(_pos))

        # recalculate the propery positions
        #for prop in self.element.properties:
        #    prop.pos = tuple(totuple(self.element._pos(prop.pos)))

        assert isinstance(_last_pos, Tuple), 'last pos is not a Tuple'
        assert isinstance(self.element.pos, Tuple), 'element pos is not a Tuple'
        return (self, self.element, _last_pos)

    def anchor(self, number: str|int = 1):
        _number = number if isinstance(number, str) else str(number)
        self._anchor = _number
        return self

    def at(self, pos: POS_T|DrawElement):
        if isinstance(pos, Pin):
            self.pos = tuple(totuple(cast(Pin, pos)._pos()[1]))
        elif isinstance(pos, DrawElement):
            draw_element = cast(DrawElement, pos)
            assert draw_element.element, 'element is None'
            self.pos = cast(PositionalElement, draw_element.element).pos
        else:
            self.pos = pos
        return self

    def rotate(self, angle: int):
        self._angle = angle
        return self

    def right(self):
        self._angle = 90
        return self

    def left(self):
        self._angle = 270
        return self

    def up(self):
        self._angle = 0
        return self

    def down(self):
        self._angle = 180
        return self

