from typing import Optional, Tuple, cast

import numpy as np

from nukleus import Library
from nukleus.model import POS_T, PinImpl, PositionalElement, Wire, Symbol
from ..model.Utils import transform, add, mul, totuple

from .DrawElement import DrawElement

ORIENTATION = {
    'left': np.array([1, 0]),
    'right': np.array([-1, 0]),
    'up': np.array([0, -1]),
    'down': np.array([0, 1])
}


class Line(DrawElement):
    """Place a connection on the schematic."""
    def __init__(self):
        self.pos: POS_T | None = None
        self._length: float = 0.0
        self._rel_length_x: float = 0
        self._rel_length_y: float = 0
        self.orientation = 'left'
        self.element: Optional[Wire] = None

    def _get(self, library: Library, last_pos: POS_T, unit: float):
        _pos: POS_T = self.pos if self.pos is not None else last_pos
        _end_pos: POS_T = (0, 0)
        if self._rel_length_x != 0:
            _end_pos = (self._rel_length_x, _pos[1])
        elif self._rel_length_y != 0:
            _end_pos = (_pos[0], self._rel_length_y)
        else:
            l = unit if self._length == 0 else self._length
            _end_pos = add(_pos, mul(ORIENTATION[self.orientation], (l, l)))

        assert isinstance(_pos, Tuple), f'_pos is not a tuple : {type(_pos)}'
        assert isinstance(
            _end_pos, Tuple), f'_pos is not a tuple : {type(_end_pos)}'
        self.element = Wire(pts=[_pos, _end_pos])
        return (self, self.element, self.element.pts[1], None)

    def at(self, pos: POS_T | PinImpl | DrawElement):
        """
        Position of the element.
        The position can either be the xy coordinates
        or a DrawElement.

        :param pos POS_T|DrawElement: Position.
        """
        if isinstance(pos, PinImpl):
            pin_impl = cast(PinImpl, pos)
            _pos = transform(cast(Symbol, pin_impl.parent), transform(pin_impl))
            self.pos = tuple(totuple(_pos[0]))
        elif isinstance(pos, DrawElement):
            assert pos.element and isinstance(pos.element, PositionalElement)
            self.pos = cast(PositionalElement, pos.element).pos
        else:
            self.pos = tuple(totuple(pos))
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
            self._rel_length_x = tuple(totuple(pos[0]))[0]
        elif isinstance(pos, DrawElement):
            assert pos.element and isinstance(pos.element, PositionalElement)
            self._rel_length_x = cast(PositionalElement, pos.element).pos[0]
        else:
            self._rel_length_x = tuple(totuple(pos))[0]
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

    def length(self, length: float):
        """
        Length of the line.

        :param pos float: Length of the line.
        """
        self._length = length
        return self

    def right(self):
        """
        Orientation of the line.

        """
        self.orientation = 'right'
        return self

    def left(self):
        """
        Orientation of the line.

        """
        self.orientation = 'left'
        return self

    def up(self):
        """
        Orientation of the line.

        """
        self.orientation = 'up'
        return self

    def down(self):
        """
        Orientation of the line.

        """
        self.orientation = 'down'
        return self
