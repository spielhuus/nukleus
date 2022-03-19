from typing import Optional, Tuple, cast

import numpy as np

from ..Library import Library
from ..model.LibrarySymbol import LibrarySymbol
from ..model.Property import Property
from ..model.Pin import Pin, PinImpl
from ..model.SchemaElement import POS_T
from ..model.PositionalElement import PositionalElement
from ..model.Symbol import Symbol, pinPosition, placeFields
from .DrawElement import DrawElement, PinNotFoundError, totuple


class Element(DrawElement):
    """Draw an elemet to the schematic"""

    def __init__(self, ref, lib_name, value=None, unit=1, **kwargs):
        self.ref = ref
        self.lib_name = lib_name
        self._value = value
        self.unit = unit
        self.properties = kwargs

        self.pos = None
        self._anchor: str = '0'
        self._angle = 0
        self._mirror = ''
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
        """
        Pin position.

        :param number int: Pin number.
        :rtype POS_T: Pin position.
        """
        assert self.element is not None
        return self.element._pos(self._pin(number)._pos())[0]

    def _get(self, library: Library, last_pos: POS_T, _: float):
        self.library_symbol = library.get(self.lib_name)
        self.library_symbol.identifier = self.lib_name
        self.element = Symbol.new(self.ref, self.lib_name, self.library_symbol)
        self.element.unit = self.unit
        self.element.angle = self._angle
        self.element.mirror = self._mirror
        self.element.property("Reference").value = self.ref
        if self._value:
            self.element.property("Value").value = self._value

        for name, value in self.properties.items():
            if name == 'on_schema':
                self.element.on_schema = bool(value)
            elif self.element.has_property(name):
                self.element.property(name).value = value
            else:
                new_property = Property(key=name, value=value)
                self.element.properties.append(new_property)

        if self.lib_name == "Device:R":
            if not self.element.has_property('Spice_Netlist_Enabled'):
                self.element.properties.append(
                    Property(key='Spice_Netlist_Enabled', value='Y'))
            if not self.element.has_property('Spice_Primitive'):
                self.element.properties.append(
                    Property(key='Spice_Primitive', value='R'))

        # get the anchor pins
        pins = self.element.getPins()
        _pin_numbers = [x.number[0] for x in pins]
        if self._anchor == '0' and len(pins) > 0:
            self._anchor = _pin_numbers[-1]

        # calculate position
        _pos = self.pos if self.pos is not None else last_pos
        self.element.pos = tuple(totuple(_pos -
                                         self.element._pos(pins[self._anchor]._pos())[0]))
        # when the anchor pin is found, set the next pos
        if self._anchor != '0':
            _last_pos = tuple(totuple(self.element._pos(
                self._pin(_pin_numbers[0])._pos())[0]))
        else:
            _last_pos = tuple(totuple(_pos))

        # recalculate the propery positions
        placeFields(self.element)

        assert isinstance(_last_pos, Tuple), 'last pos is not a Tuple'
        assert isinstance(self.element.pos,
                          Tuple), 'element pos is not a Tuple'
        return (self, self.element, _last_pos)

    def anchor(self, number: str | int = 1):
        """
        Anchor the symbol on a pin.

        :param number str|int: Pin by number.
        """
        _number = number if isinstance(number, str) else str(number)
        self._anchor = _number
        return self

    def at(self, pos: POS_T | DrawElement):
        """
        Position the element at a position.
        The position can either be the xy coordinates
        or a DrawElement.

        :param pos POS_T|DrawElement: Position.
        """
        if isinstance(pos, PinImpl):
            pin_impl = cast(PinImpl, pos)
            _parent = pin_impl.parent
            _pos = cast(Symbol, _parent)._pos(pin_impl._pos())
            self.pos = tuple(totuple(_pos[0]))
        elif isinstance(pos, DrawElement):
            draw_element = cast(DrawElement, pos)
            assert draw_element.element, 'element is None'
            self.pos = cast(PositionalElement, draw_element.element).pos
        else:
            self.pos = pos
        return self

    def rotate(self, angle: float):
        """
        Rotate the symbol.

        :param angle float: Rotation angle in degree.
        """
        self._angle = angle
        return self

    def right(self):
        """
        Orietation of the symbol.

        """
        self._angle = 90
        return self

    def left(self):
        """
        Orietation of the symbol.

        """
        self._angle = 270
        return self

    def up(self):
        """
        Orietation of the symbol.

        """
        self._angle = 0
        return self

    def down(self):
        """
        Orietation of the symbol.

        """
        self._angle = 180
        return self

    def mirror(self, axis: str):
        """
        Mirror the symbol.

        :param axis str: mirror the symbol by x or y axis.
        """
        self._mirror = axis
        return self
