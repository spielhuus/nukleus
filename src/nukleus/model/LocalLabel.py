from __future__ import annotations

from typing import List, cast

from .Utils import ffmt
from .SchemaElement import POS_T
from .PositionalElement import PositionalElement
from .TextEffects import TextEffects
from ..SexpParser import SEXP_T

class LocalLabel(PositionalElement):
    """
    The label token defines an wire or bus label name in a schematic.
    """
    def __init__(self, **kwargs) -> None:
        self.text = kwargs.get('text', '')
        """The TEXT is a quoted string that defines the label."""
        self.text_effects = kwargs.get('text_effects', TextEffects())
        """The TEXT_EFFECTS section defines how the label text is drawn."""
        super().__init__(kwargs.get('identifier', None),
                         kwargs.get('pos', ((0, 0), (0, 0))),
                         kwargs.get('angle', 0))

    @classmethod
    def parse(cls, sexp: SEXP_T) -> LocalLabel:
        """Parse the sexp input.

        :param sexp SEXP_T: Sexp as List.
        :rtype LocalLabel: The LocalLabel Object.
        """
        _identifier = None
        _pos: POS_T = (0, 0)
        _angle: float = 0
        _text: str = cast(str, sexp[1])
        _text_effects: TextEffects = TextEffects()

        for token in sexp[2:]:
            if token[0] == 'at':
                _pos = (float(token[1]), float(token[2]))
                if len(token) == 4:
                    _angle = float(token[3])
            elif token[0] == 'uuid':
                _identifier = token[1]
            elif token[0] == 'effects':
                _text_effects = TextEffects.parse(cast(SEXP_T, token))
            else:
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
            f'(at {self.pos[0]:g} {ffmt(self.pos[1])} {ffmt(self.angle)})')
        strings.append(self.text_effects.sexp(indent=indent+1))
        strings.append(f'{"  " * (indent + 1)}(uuid {self.identifier})')
        strings.append(f'{"  " * indent})')
        return "\n".join(strings)
