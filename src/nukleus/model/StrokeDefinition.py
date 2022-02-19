from __future__ import annotations

from typing import Any, List

from ..SexpParser import SEXP_T
from .rgb import rgb


class StrokeDefinition():
    """
    The stroke token defines how the outlines of graphical objects are drawn.
    """
    width: float
    type: str
    color: rgb

    def __init__(self, **kwargs) -> None:
        self.width = kwargs.get('width', 0)
        self.type = kwargs.get('type', '')
        self.color = kwargs.get('color', rgb(0, 0, 0, 0))

    @classmethod
    def parse(cls, sexp: SEXP_T) -> StrokeDefinition:
        _width: float = 0
        _type: str = ''
        _color: rgb = rgb(0, 0, 0, 0)

        for token in sexp[1:]:
            match token:
                case ['width', width]:
                    _width = float(width)
                case ['type', stype]:
                    _type = stype
                case ["color", *color]:
                    _color = rgb(*[int(i) for i in color])
                case _:
                    raise ValueError(f"unknown stroke element {token}")

        return StrokeDefinition(width=_width, type=_type, color=_color)

    def sexp(self, indent: int = 1) -> str:
        """
        Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        strings: List[str] = []
        strings.append(f'{"  " * indent}(stroke ')
        strings.append(f'(width {self.width:g}) ')
        strings.append(f'(type {self.type}) ')
        strings.append(f'(color {self.color.r} {self.color.g} '
                       f'{self.color.b} {self.color.a}))')
        return "".join(strings)

    def __eq__(self, other: Any) -> Any:
        return self.width == other.width and \
            self.type == other.type and \
            self.color == other.color
