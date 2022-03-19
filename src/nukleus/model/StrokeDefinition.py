from __future__ import annotations

from typing import Any, List

from ..SexpParser import SEXP_T
from .rgb import rgb
from .Utils import ffmt


class StrokeDefinition():
    """
    The stroke token defines how the outlines of graphical objects are drawn.
    """
    def __init__(self, **kwargs) -> None:
        self.width = kwargs.get('width', 0)
        """The width token attribute defines the line width of the graphic object."""
        self.stroke_type = kwargs.get('stroke_type', '')
        """The type token attribute defines the line style of the graphic object.
        Valid stroke line styles are:
        -dash
        -dash_dot
        -dash_dot_dot (version 7)
        -dot
        -default
        -solid"""
        self.color = kwargs.get('color', rgb(0, 0, 0, 0))
        """The color token attributes define the line red, green, blue, and alpha color settings."""

    @classmethod
    def parse(cls, sexp: SEXP_T) -> StrokeDefinition:
        """Parse the sexp input.

        :param sexp SEXP_T: Sexp as List.
        :rtype StrokeDefinition: The StrokeDefinition Object.
        """
        _width: float = 0
        _type: str = ''
        _color: rgb = rgb(0, 0, 0, 0)

        for token in sexp[1:]:
            if token[0] == 'width':
                _width = float(token[1])
            elif token[0] == 'type':
                _type = token[1]
            elif token[0] == 'color':
                _color = rgb(float(token[1]), float(
                    token[2]), float(token[3]), float(token[4]))
            else:
                raise ValueError(f"unknown StrokeDefinition element {token}")

        return StrokeDefinition(width=_width, stroke_type=_type, color=_color)

    def sexp(self, indent: int = 1) -> str:
        """Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        strings: List[str] = []
        strings.append(f'{"  " * indent}(stroke ')
        strings.append(f'(width {self.width:g}) ')
        strings.append(f'(type {self.stroke_type}) ')
        strings.append(f'(color {ffmt(self.color.r)} {ffmt(self.color.g)} '
                       f'{ffmt(self.color.b)} {ffmt(self.color.a)}))')
        return "".join(strings)

    def __eq__(self, other: Any) -> Any:
        return self.width == other.width and \
            self.stroke_type == other.stroke_type and \
            self.color == other.color
