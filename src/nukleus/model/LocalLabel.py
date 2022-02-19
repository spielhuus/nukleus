from __future__ import annotations

from typing import List

import uuid

from .PositionalElement import PositionalElement, POS_T
from .TextEffects import TextEffects
from ..SexpParser import SEXP_T

class LocalLabel(PositionalElement):
    """
    The label token defines an wire or bus label name in a schematic.
    """
    text: str
    text_effects: TextEffects



    def __init__(self, **kwargs) -> None:
        self.text = kwargs.get('text', '')
        self.text_effects = kwargs.get('text_effects', ('', TextEffects()))
        super().__init__(kwargs.get('identifier', None),
                         kwargs.get('pos', ((0, 0), (0, 0))),
                         kwargs.get('angle', 0))

    @classmethod
    def parse(cls, sexp: SEXP_T) -> LocalLabel:
        _identifier = None
        _pos: POS_T = (0, 0)
        _angle: float = 0
        _text: str = sexp[1]
        _text_effects: TextEffects = TextEffects()

        for token in sexp[2:]:
            match token:
                case ['at', x, y, angle]:
                    _pos = (float(x), float(y))
                    _angle = float(angle)
                case ['at', x, y]:
                    _pos = (float(x), float(y))
                case ['uuid', identifier]:
                    _identifier = identifier
                case ['effects', *_]:
                    _text_effects = TextEffects.parse(token)
                case _:
                    raise ValueError(f"unknown label element {token}")

        return LocalLabel(identifier=_identifier, pos=_pos, angle=_angle,
                        text=_text, text_effects=_text_effects)

    def sexp(self, indent: int=1) -> str:
        """
        Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        strings: List[str] = []
        strings.append(
            f'{"  " * indent}(label "{self.text}" '
            f'(at {self.pos[0]:g} {self.pos[1]:g} {self.angle:g})')
        strings.append(self.text_effects.sexp(indent=indent+1))
        strings.append(f'{"  " * (indent + 1)}(uuid {self.identifier})')
        strings.append(f'{"  " * indent})')
        return "\n".join(strings)
