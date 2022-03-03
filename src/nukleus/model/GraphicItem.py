from __future__ import annotations

from typing import List, Tuple

from ..SexpParser import SEXP_T
from .FillType import FillType, get_fill_str, get_fill_type
from .PositionalElement import POS_T
from .StrokeDefinition import StrokeDefinition


class GraphicItem():
    """Abstract Class for a GraphicItem."""
    fill: FillType
    """ Fill type of the Graphic"""

    def __init__(self, fill) -> None:
        self.fill = fill

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
        self.points: List[Tuple[float, float]] = kwargs.get('points', [])
        self.stroke_definition: StrokeDefinition = kwargs.get(
            'stroke_definition', StrokeDefinition())
        super().__init__(kwargs.get('fill', FillType.NONE))

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
            match token:
                case ['pts', *_]:
                    for _pt in token:
                        match _pt:
                            case ['xy', x, y]:
                                _points.append((float(x), float(y)))
                case ['stroke', *_]:
                    _stroke_definition = StrokeDefinition.parse(token)
                case ['fill', ['type', fill]]:
                    _fill = get_fill_type(fill)
                case _:
                    raise ValueError(f"unknown polyline element {token}")

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
        for p in self.points:
            strings.append(f'{"  " * (indent + 2)}(xy {p[0]:g} {p[1]:g})')
        strings.append(f'{"  " * (indent + 1)})')
        strings.append(self.stroke_definition.sexp(indent=indent+1))
        strings.append(
            f'{"  " * (indent + 1)}(fill (type {get_fill_str(self.fill)}))')
        strings.append(f'{"  " * indent})')
        return "\n".join(strings)


class Rectangle(GraphicItem):
    start_x: float
    start_y: float
    end_x: float
    end_y: float
    stroke_definition: StrokeDefinition

    def __init__(self, **kwargs) -> None:
        self.start_x: float = kwargs.get('start_x', 0)
        self.start_y: float = kwargs.get('start_y', 0)
        self.end_x: float = kwargs.get('end_x', 0)
        self.end_y: float = kwargs.get('end_y', 0)
        self.stroke_definition: StrokeDefinition = kwargs.get(
            'stroke_definition', StrokeDefinition())
        super().__init__(kwargs.get('fill', FillType.NONE))

    @classmethod
    def parse(cls, sexp: SEXP_T) -> Rectangle:
        _start_x: float = 0
        _start_y: float = 0
        _end_x: float = 0
        _end_y: float = 0
        _fill: FillType = FillType.NONE
        _stroke_definition: StrokeDefinition = StrokeDefinition()

        for token in sexp[1:]:
            match token:
                case ['start', x, y]:
                    _start_x = float(x)
                    _start_y = float(y)
                case ['end', x, y]:
                    _end_x = float(x)
                    _end_y = float(y)
                case ['stroke', *_]:
                    _stroke_definition = StrokeDefinition.parse(token)
                case ['fill', ['type', fill]]:
                    _fill = get_fill_type(fill)
                case _:
                    raise ValueError(f"unknown polyline element {token}")

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
    center: POS_T
    radius: float
    stroke_definition: StrokeDefinition

    def __init__(self, **kwargs) -> None:
        self.center: float = kwargs.get('center', 0)
        self.radius: float = kwargs.get('radius', 0)
        self.stroke_definition: StrokeDefinition = kwargs.get(
            'stroke_definition', StrokeDefinition())
        super().__init__(kwargs.get('fill', FillType.NONE))

    @classmethod
    def parse(cls, sexp: SEXP_T) -> Circle:
        _center: POS_T = (0, 0)
        _radius: float = 0
        _fill: FillType = FillType.NONE
        _stroke_definition: StrokeDefinition = StrokeDefinition()

        for token in sexp[1:]:
            match token:
                case ['center', x, y]:
                    _center = (float(x), float(y))
                case ['radius', r]:
                    _radius = float(r)
                case ['stroke', *_]:
                    _stroke_definition = StrokeDefinition.parse(token)
                case ['fill', ['type', fill]]:
                    _fill = get_fill_type(fill)
                case _:
                    raise ValueError(f"unknown polyline element {token}")

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
    start: POS_T
    mid: POS_T
    end: POS_T
    stroke_definition: StrokeDefinition

    def __init__(self, **kwargs) -> None:
        self.start: float = kwargs.get('start', (0, 0))
        self.mid: float = kwargs.get('mid', (0, 0))
        self.end: float = kwargs.get('end', (0, 0))
        self.stroke_definition: StrokeDefinition = kwargs.get(
            'stroke_definition', StrokeDefinition())
        super().__init__(kwargs.get('fill', FillType.NONE))

    @classmethod
    def parse(cls, sexp: SEXP_T) -> Arc:
        _start: POS_T = (0, 0)
        _mid: POS_T = (0, 0)
        _end: POS_T = (0, 0)
        _fill: FillType = FillType.NONE
        _stroke_definition: StrokeDefinition = StrokeDefinition()

        for token in sexp[1:]:
            match token:
                case ['start', x, y]:
                    _start = (float(x), float(y))
                case ['mid', x, y]:
                    _mid = (float(x), float(y))
                case ['end', x, y]:
                    _end = (float(x), float(y))
                case ['stroke', *_]:
                    _stroke_definition = StrokeDefinition.parse(token)
                case ['fill', ['type', fill]]:
                    _fill = get_fill_type(fill)
                case _:
                    raise ValueError(f"unknown polyline element {token}")

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
