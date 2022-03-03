from __future__ import annotations

from dataclasses import dataclass
from typing import List, cast

import uuid

from .PositionalElement import PositionalElement
from .StrokeDefinition import StrokeDefinition
from .TextEffects import TextEffects
from .Utils import ffmt
from ..SexpParser import SEXP_T

@dataclass
class GraphicalText(PositionalElement):
    """
    The text token defines graphical text in a schematic.
    """
    text: str
    text_effects: TextEffects

    def __init__(self, **kwargs) -> None:
        self.text = kwargs.get('text', '')
        self.text_effects = kwargs.get('text_effects', TextEffects())
        super().__init__(
            kwargs.get("identifier", None),
            kwargs.get("pos", ((0, 0), (0, 0))),
            kwargs.get("angle", 0),
        )

    @classmethod
    def parse(cls, sexp: SEXP_T) -> GraphicalText:
        _text = sexp[1]
        _text_effects = ''
        _identifier = ''
        _pos = (0, 0)
        _angle = 0

        for token in sexp[2:]:
            match token:
                case ['at', x, y, angle]:
                    _pos = (float(x), float(y))
                    _angle = float(angle)
                case ['at', x, y]:
                    _pos = (float(x), float(y))
                case ["uuid", identifier]:
                    _identifier = identifier
                case ["effects", *_]:
                    _text_effects = TextEffects.parse(cast(SEXP_T, token))
                case _:
                    raise ValueError(f"unknown property element {token}")


        return GraphicalText(text=_text, text_effects=_text_effects, pos=_pos, angle=_angle,
                   identifier=_identifier)

    def sexp(self, indent: int=1) -> str:
        """
        Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        strings: List[str] = []
        strings.append( f'{"  " * indent}(text "{self.text}" (at {ffmt(self.pos[0])} {ffmt(self.pos[1])} {ffmt(self.angle)})')
        strings.append(self.text_effects.sexp(indent=indent+1))
        strings.append(f'{"  " * (indent+1)}(uuid {self.identifier})')
        strings.append(f'{"  " * indent})')
        return "\n".join(strings)
