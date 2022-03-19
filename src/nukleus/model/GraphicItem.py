from __future__ import annotations

from typing import List, Tuple, cast

import numpy as np

from nukleus.model.TextEffects import TextEffects

from .FillType import FillType, get_fill_str, get_fill_type
from .SchemaElement import POS_T, PTS_T
from .StrokeDefinition import StrokeDefinition
from .Utils import ffmt
from ..SexpParser import SEXP_T


def f_coord(arr): 
    return [(np.min(arr[..., 0]), np.min(arr[..., 1])),
            (np.max(arr[..., 0]), np.max(arr[..., 1]))]


class GraphicItem():
    """Abstract Class for a GraphicItem."""

    def __init__(self, fill) -> None:
        self.fill: FillType = fill

    @classmethod
    def sexp(cls, indent: int = 1) -> str:
        """
        Create sexp string from the object.

        :param indent int: indent count.
        :rtype str: sexp string.
        """
        assert False, f'abstract method called with indent: {indent}'


class Polyline(GraphicItem):
    '''
    Polyline
    Draw a polyline.

    args:
        :arg fill FillType: fill type
        :arg points Tuple[float, float]: Coordinates of the line
        :arg stroke_definition StrokeDefinition: Line description.
    '''
    points: List[Tuple[float, float]]
    stroke_definition: StrokeDefinition

    def __init__(self, **kwargs) -> None:
        self.points: PTS_T = kwargs.get('points', [])
        self.stroke_definition: StrokeDefinition = kwargs.get(
            'stroke_definition', StrokeDefinition())
        super().__init__(kwargs.get('fill', FillType.NONE))

    def size(self) -> List[float]:
        return f_coord(np.array(self.points))

    @classmethod
    def parse(cls, sexp: SEXP_T) -> Polyline:
        """
        Parse the sexp input.

        :param sexp SEXP_T: Sexp as List.
        :rtype Polyline: The Polyline Object.
        """
        _fill: FillType = FillType.NONE
        _points: List[Tuple[float, float]] = []
        _stroke_definition: StrokeDefinition = StrokeDefinition()

        for token in sexp[1:]:
            if token[0] == 'pts':
                for _pts in token[1:]:
                    _points.append((float(_pts[1]), float(_pts[2])))
            elif token[0] == 'stroke':
                _stroke_definition = StrokeDefinition.parse(cast(SEXP_T, token))
            elif token[0] == 'fill' and token[1][0] == 'type':
                _fill = get_fill_type(token[1][1])
            else:
                raise ValueError(f"unknown Polyline element {token}")

        return Polyline(fill=_fill, points=_points, stroke_definition=_stroke_definition)

    def sexp(self, indent: int = 1) -> str:
        """
        Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        strings: List[str] = []
        strings.append(f'{"  " * indent}(polyline')
        strings.append(f'{"  " * (indent + 1)}(pts')
        for _pts in self.points:
            strings.append(f'{"  " * (indent + 2)}(xy {ffmt(_pts[0])} {ffmt(_pts[1])})')
        strings.append(f'{"  " * (indent + 1)})')
        strings.append(self.stroke_definition.sexp(indent=indent+1))
        strings.append(
            f'{"  " * (indent + 1)}(fill (type {get_fill_str(self.fill)}))')
        strings.append(f'{"  " * indent})')
        return "\n".join(strings)


class Rectangle(GraphicItem):
    """The rectangle token defines a graphical rectangle in a symbol definition."""
    def __init__(self, **kwargs) -> None:
        self.start_x: float = kwargs.get('start_x', 0)
        self.start_y: float = kwargs.get('start_y', 0)
        self.end_x: float = kwargs.get('end_x', 0)
        self.end_y: float = kwargs.get('end_y', 0)
        self.stroke_definition: StrokeDefinition = kwargs.get(
            'stroke_definition', StrokeDefinition())
        super().__init__(kwargs.get('fill', FillType.NONE))

    def size(self) -> List[float]:
        return np.array([(self.start_x, self.start_y), (self.end_x, self.end_y)])

    @classmethod
    def parse(cls, sexp: SEXP_T) -> Rectangle:
        """Parse the sexp input.

        :param sexp SEXP_T: Sexp as List.
        :rtype Rectangle: The Rectangle Object.
        """
        _start_x: float = 0
        _start_y: float = 0
        _end_x: float = 0
        _end_y: float = 0
        _fill: FillType = FillType.NONE
        _stroke_definition: StrokeDefinition = StrokeDefinition()

        for token in sexp[1:]:
            if token[0] == 'start':
                _start_x = float(token[1])
                _start_y = float(token[2])
            elif token[0] == 'end':
                _end_x = float(token[1])
                _end_y = float(token[2])
            elif token[0] == 'stroke':
                _stroke_definition = StrokeDefinition.parse(cast(SEXP_T, token))
            elif token[0] == 'fill' and token[1][0] == 'type':
                _fill = get_fill_type(token[1][1])
            else:
                raise ValueError(f"unknown Rectangle element {token}")

        return Rectangle(start_x=_start_x, start_y=_start_y, end_x=_end_x, end_y=_end_y,
                         fill=_fill, stroke_definition=_stroke_definition)

    def sexp(self, indent: int = 1) -> str:
        """
        Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        strings: List[str] = []
        strings.append(f'{"  " * indent}(rectangle (start '
                       f'{self.start_x:g} {self.start_y:g})'
                       f' (end {self.end_x:g} {self.end_y:g})')
        strings.append(self.stroke_definition.sexp(indent=indent+1))
        strings.append(
            f'{"  " * (indent + 1)}(fill (type {get_fill_str(self.fill)}))')
        strings.append(f'{"  " * indent})')
        return "\n".join(strings)


class Circle(GraphicItem):
    """ The circle token defines a graphical circle in a symbol definition. """

    def __init__(self, **kwargs) -> None:
        self.center: POS_T = kwargs.get('center', 0)
        self.radius: float = kwargs.get('radius', 0)
        self.stroke_definition: StrokeDefinition = kwargs.get(
            'stroke_definition', StrokeDefinition())
        super().__init__(kwargs.get('fill', FillType.NONE))

    @classmethod
    def parse(cls, sexp: SEXP_T) -> Circle:
        """Parse the sexp input.

        :param sexp SEXP_T: Sexp as List.
        :rtype Circle: The Circle Object.
        """
        _center: POS_T = (0, 0)
        _radius: float = 0
        _fill: FillType = FillType.NONE
        _stroke_definition: StrokeDefinition = StrokeDefinition()

        for token in sexp[1:]:
            if token[0] == 'center':
                _center = (float(token[1]), float(token[2]))
            elif token[0] == 'radius':
                _radius = float(token[1])
            elif token[0] == 'stroke':
                _stroke_definition = StrokeDefinition.parse(cast(SEXP_T, token))
            elif token[0] == 'fill' and token[1][0] == 'type':
                _fill = get_fill_type(token[1][1])
            else:
                raise ValueError(f"unknown Circle element {token}")

        return Circle(center=_center, radius=_radius,
                      fill=_fill, stroke_definition=_stroke_definition)

    def sexp(self, indent: int = 1) -> str:
        """
        Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        # TODO
        strings: List[str] = []
        return "\n".join(strings)


class Arc(GraphicItem):
    """ The arc token defines a graphical arc in a symbol definition. """

    def __init__(self, **kwargs) -> None:
        self.start: float = kwargs.get('start', (0, 0))
        self.mid: float = kwargs.get('mid', (0, 0))
        self.end: float = kwargs.get('end', (0, 0))
        self.stroke_definition: StrokeDefinition = kwargs.get(
            'stroke_definition', StrokeDefinition())
        super().__init__(kwargs.get('fill', FillType.NONE))

    @classmethod
    def parse(cls, sexp: SEXP_T) -> Arc:
        """Parse the sexp input.

        :param sexp SEXP_T: Sexp as List.
        :rtype Arc: The Arc Object.
        """
        _start: POS_T = (0, 0)
        _mid: POS_T = (0, 0)
        _end: POS_T = (0, 0)
        _fill: FillType = FillType.NONE
        _stroke_definition: StrokeDefinition = StrokeDefinition()

        for token in sexp[1:]:
            if token[0] == 'start':
                _start = (float(token[1]), float(token[2]))
            elif token[0] == 'mid':
                _mid = (float(token[1]), float(token[2]))
            elif token[0] == 'end':
                _end = (float(token[1]), float(token[2]))
            elif token[0] == 'stroke':
                _stroke_definition = StrokeDefinition.parse(cast(SEXP_T, token))
            elif token[0] == 'fill' and token[1][0] == 'type':
                _fill = get_fill_type(token[1][1])
            else:
                raise ValueError(f"unknown Arc element {token}")

        return Arc(start=_start, mid=_mid, end=_end,
                   fill=_fill, stroke_definition=_stroke_definition)

    def sexp(self, indent: int = 1) -> str:
        """
        Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        # TODO
        strings: List[str] = []
        return "\n".join(strings)

class Text(GraphicItem):
    """The text token defines graphical text in a symbol definition."""

    def __init__(self, **kwargs) -> None:
        self.pos: POS_T = kwargs.get('pos', (0, 0))
        self.angle: float = kwargs.get('angle', 0)
        self.text: str = kwargs.get('text', '')
        self.text_effects: TextEffects|None = kwargs.get('text_effects', None)
        super().__init__(None)

    @classmethod
    def parse(cls, sexp: SEXP_T) -> Arc:
        """Parse the sexp input.

        :param sexp SEXP_T: Sexp as List.
        :rtype Text: The Text Object.
        """
        _pos: POS_T = (0, 0)
        _angle: float = 0
        _text: str = str(sexp[1])
        _text_effects: TextEffects|None = None

        for token in sexp[2:]:
            if token[0] == 'at':
                _pos = (float(token[1]), float(token[2]))
                if len(token) == 4:
                    _angle = float(token[3])
            elif token[0] == 'text':
                _text = token[1]
            elif token[0] == 'effects':
                _text_effects = TextEffects.parse(cast(SEXP_T, token))
            else:
                raise ValueError(f"unknown Text element {token}")

        return Arc(pos=_pos, angle=_angle, text=_text,
                   text_effects=_text_effects)

    def sexp(self, indent: int = 1) -> str:
        """
        Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        # TODO
        strings: List[str] = []
        return "\n".join(strings)
