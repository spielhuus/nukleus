from __future__ import annotations

from typing import List, cast

from .PositionalElement import PositionalElement, ffmt
from .TextEffects import TextEffects
from ..SexpParser import SEXP_T

class GraphicalText(PositionalElement):
    """
    The text token defines graphical text in a schematic.
    """
    def __init__(self, **kwargs) -> None:
        self.text = kwargs.get('text', '')
        """The TEXT is a quoted string that defines the text."""
        self.text_effects = kwargs.get('text_effects', TextEffects())
        """The TEXT_EFFECTS section defines how the text is drawn."""
        super().__init__(
            kwargs.get("identifier", None),
            kwargs.get("pos", ((0, 0), (0, 0))),
            kwargs.get("angle", 0),
        )

    @classmethod
    def parse(cls, sexp: SEXP_T) -> GraphicalText:
        """Parse the sexp input.

        :param sexp SEXP_T: Sexp as List.
        :rtype GraphicalText: The GraphicalText Object.
        """
        _text = sexp[1]
        _text_effects = ''
        _identifier = ''
        _pos = (0, 0)
        _angle = 0

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
                raise ValueError(f"unknown GraphicalText element {token}")

        return GraphicalText(text=_text, text_effects=_text_effects, pos=_pos, angle=_angle,
                   identifier=_identifier)

    def sexp(self, indent: int=1) -> str:
        """
        Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        strings: List[str] = []
        strings.append( f'{"  " * indent}(text "{self.text}" (at {ffmt(self.pos[0])} '
                        f'{ffmt(self.pos[1])} {ffmt(self.angle)})')
        strings.append(self.text_effects.sexp(indent=indent+1))
        strings.append(f'{"  " * (indent+1)}(uuid {self.identifier})')
        strings.append(f'{"  " * indent})')
        return "\n".join(strings)
