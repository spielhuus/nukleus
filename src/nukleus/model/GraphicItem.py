from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple

from .PositionalElement import POS_T
from .StrokeDefinition import StrokeDefinition


class FillType(Enum):
    FOREGROUND = 1
    BACKGROUND = 2
    NONE = 3


def get_fill_str(type: FillType) -> str:
    if type == FillType.FOREGROUND:
        return 'outline'
    elif type == FillType.BACKGROUND:
        return 'background'
    else:
        return 'none'


def get_fill_type(type: str) -> FillType:
    if type == 'outline':
        return FillType.FOREGROUND
    elif type == 'background':
        return FillType.BACKGROUND
    else:
        return FillType.NONE


@dataclass
class GraphicItem(ABC):
    """Abstract Class for a GraphicItem."""
    fill: FillType
    """ Fill type of the Graphic"""

    @abstractmethod
    def sexp(self, indent=1) -> str:
        pass


@dataclass
class Polyline(GraphicItem):
    points: List[Tuple[float, float]]
    stroke_definition: StrokeDefinition

    def sexp(self, indent=1) -> str:
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
        return "\r\n".join(strings)


@dataclass
class Rectangle(GraphicItem):
    start_x: int
    start_y: int
    end_x: int
    end_y: int
    stroke_definition: StrokeDefinition

    def sexp(self, indent=1) -> str:
        strings: List[str] = []
        strings.append(f'{"  " * indent}(rectangle (start '
                       f'{self.start_x:g} {self.start_y:g})'
                       f' (end {self.end_x:g} {self.end_y:g})')
        strings.append(self.stroke_definition.sexp(indent=indent+1))
        strings.append(
            f'{"  " * (indent + 1)}(fill (type {get_fill_str(self.fill)}))')
        strings.append(f'{"  " * indent})')
        return "\r\n".join(strings)


@dataclass
class Circle(GraphicItem):
    """ The circle token defines a graphical circle in a symbol definition. """
    center: POS_T
    radius: float
    stroke_definition: StrokeDefinition

    def sexp(self, indent=1) -> str:
        # TODO
        strings: List[str] = []
        return "\r\n".join(strings)


@dataclass
class Arc(GraphicItem):
    """ The arc token defines a graphical arc in a symbol definition. """
    start: POS_T
    mid: POS_T
    end: float
    stroke_definition: StrokeDefinition

    def sexp(self, indent=1) -> str:
        # TODO
        strings: List[str] = []
        return "\r\n".join(strings)
