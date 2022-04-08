from typing import Optional, Tuple, cast

from ..Library import Library
from ..model.LibrarySymbol import LibrarySymbol
from ..model.Property import Property
from ..model.Pin import Pin, PinImpl
from ..model.SchemaElement import POS_T
from ..model.PositionalElement import PositionalElement
from ..model.Symbol import Symbol
from ..model.Utils import placeFields, transform, sub, get_pins, totuple
from .DrawElement import DrawElement, PinNotFoundError
from .Line import Line


class Element(DrawElement):
    """Draw an elemet to the schematic"""

    def __init__(self, ref, lib_name, value=None, unit=1, **kwargs):
        self.ref = ref
        self.lib_name = lib_name
        self._value = value
        self.unit = unit
        self.properties = kwargs

        self.pos: POS_T|None = None
        self._anchor: str = '0'
        self._angle = 0
        self._mirror = ''
        self.library_symbol: Optional[LibrarySymbol] = None
        self.element: Optional[Symbol] = None
        self.rel_x: float = 0.0
        self.rel_y: float = 0.0

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
        return transform(self.element, transform(self._pin(number)))[0]

    def _get(self, library: Library, last_pos: POS_T, _: float):
        self.library_symbol = library.get(self.lib_name)
        self.library_symbol.identifier = self.lib_name
        self.element = Symbol.new(self.ref, self.lib_name, self.library_symbol)
        self.element.unit = self.unit
        self.element.angle = self._angle
        extra_elements = []
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
        pins = get_pins(self.element)
        _pin_numbers = [x.number[0] for x in pins]
        if self._anchor == '0' and len(pins) > 0:
            self._anchor = _pin_numbers[0]


        # calculate position
        _pos = self.pos if self.pos is not None else last_pos
        self.element.pos = sub(_pos, transform(self.element, transform(pins[self._anchor])))[0]
        # calculate tox and toy

        if self.rel_x != 0 or self.rel_y != 0:
            startx = transform(self.element, transform(pins['1']))[0][0]
            starty = transform(self.element, transform(pins['1']))[0][1]
            endx = transform(self.element, transform(pins['2']))[0][0]
            endy = transform(self.element, transform(pins['2']))[0][1]
            horizontal_length = startx - endx
            vertical_length = endy - starty
            print(f'element relative placement: {self.rel_x} {_pos} {horizontal_length}')
            if self.rel_x != 0:
                self.element.pos = ( self.element.pos[0] - ((_pos[0] - self.rel_x - horizontal_length) / 2), self.element.pos[1])
                line = Line().at(_pos).length(((_pos[0] - self.rel_x - horizontal_length) / 2)).right()
                extra_elements.append(line)
                endx = transform(self.element, transform(pins['2']))[0][0]
                endy = transform(self.element, transform(pins['2']))[0][1]
                line = Line().at((endx, endy)).length(((_pos[0] - self.rel_x - horizontal_length) / 2)).right()
                extra_elements.append(line)
            elif self.rel_y != 0:
                self.pos = (last_pos[0], last_pos[1] + self.rel_y)

        # when the anchor pin is found, set the next pos
        if len(pins) > 1:
            for pin in _pin_numbers:
                if str(self._anchor) != str(pin):
                    _last_pos = transform(self.element,
                        transform(pins[pin]))[0]
        else:
            _last_pos = tuple(totuple(_pos))

        # recalculate the propery positions

        placeFields(self.element)

        assert isinstance(_last_pos, Tuple), 'last pos is not a Tuple'
        assert isinstance(self.element.pos,
                          Tuple), 'element pos is not a Tuple'
        return (self, self.element, _last_pos, extra_elements)

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
            _pos = transform(cast(Symbol, _parent), transform(pin_impl))
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

    def tox(self, pos):
        """
        Length of the line.
        The position can either be the xy coordinates
        or a DrawElement.

        :param pos POS_T|DrawElement: Position.
        """
        if isinstance(pos, PinImpl):
            pin_impl = cast(PinImpl, pos)
            pos = transform(cast(Symbol, pin_impl.parent), transform(pin_impl))
            self.rel_x = tuple(totuple(pos[0]))[0]
        elif isinstance(pos, DrawElement):
            assert pos.element and isinstance(pos.element, PositionalElement)
            self.rel_x = cast(PositionalElement, pos.element).pos[0]
        else:
            self.rel_x = tuple(totuple(pos))[0]
        #self._rel_length_x = pos[0][0]
        return self

    def toy(self, pos):
        """
        Length of the line.
        The position can either be the xy coordinates
        or a DrawElement.

        :param pos POS_T|DrawElement: Position.
        """
        if isinstance(pos, PinImpl):
            pin_impl = cast(PinImpl, pos)
            pos = transform(cast(Symbol, pin_impl.parent), transform(pin_impl))
            self._rel_length_y = tuple(totuple(pos[0]))[1]
        elif isinstance(pos, DrawElement):
            assert pos.element and isinstance(pos.element, PositionalElement)
            self._rel_length_y = cast(PositionalElement, pos.element).pos[1]
        else:
            self._rel_length_y = tuple(totuple(pos))[1]
        return self
