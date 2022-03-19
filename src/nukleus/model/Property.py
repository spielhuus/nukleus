from __future__ import annotations

from typing import Any, List, cast

from ..SexpParser import SEXP_T
from .SchemaElement import POS_T
from .TextEffects import TextEffects
from .Utils import ffmt


class Property:
    """
    The property token defines a key value pair for storing user defined information.
    """
    def __init__(self, **kwargs) -> None:
        self.key: str = kwargs.get("key", "")
        """The "KEY" string defines the name of the property and must be unique."""
        self.value: str = kwargs.get("value", "")
        """The "VALUE" string defines the value of the property."""
        self.pos: POS_T = kwargs.get("pos", (0, 0))
        """The POSITION_IDENTIFIER defines the X and Y coordinates
        of the property."""
        self.angle: float = kwargs.get("angle", 0)
        """The angle defines the rotation angle of the property."""
        self.id: str = kwargs.get("id", 0)
        """The id token defines an integer ID for the property and must be unique."""
        self.text_effects: TextEffects = kwargs.get("text_effects", TextEffects())
        """The TEXT_EFFECTS section defines how the text is displayed."""

    @classmethod
    def parse(cls, sexp: SEXP_T) -> Property:
        """Parse the sexp input.

        :param sexp SEXP_T: Sexp as List.
        :rtype Property: The Property Object.
        """
        _key: str = cast(str, sexp[1])
        _value: str = cast(str, sexp[2])
        _id: int = 0
        _pos: POS_T = (0, 0)
        _angle: float = 0
        _text_effects: TextEffects|None = None

        for token in sexp[3:]:
            if token[0] == 'at':
                _pos = (float(token[1]), float(token[2]))
                if len(token) == 4:
                    _angle = float(token[3])
            elif token[0] == 'id':
                _id = int(token[1])
            elif token[0] == 'effects':
                _text_effects = TextEffects.parse(cast(SEXP_T, token))
            else:
                raise ValueError(f"unknown Property element {token}")

        return Property(
            key=_key,
            value=_value,
            id=_id,
            pos=_pos,
            angle=_angle,
            text_effects=_text_effects,
        )

    def sexp(self, indent: int = 1) -> str:
        """
        Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        strings: List[str] = []
        strings.append(
            f'{"  " * indent}(property "{self.key}" "{self.value}" '
            f"(id {self.id}) (at {ffmt(self.pos[0])} {ffmt(self.pos[1])} {ffmt(self.angle)})"
        )
        if self.text_effects:
            strings.append(self.text_effects.sexp(indent=indent + 1))
            strings.append(f'{"  " * indent})')
        else:
            strings[-1] += ')'
        return "\n".join(strings)

    def __eq__(self, __o: Any) -> bool:
        return (
            self.key == __o.key
            and self.value == __o.value
            and self.id == __o.id
            and self.pos == __o.pos
            and self.angle == __o.angle
            and self.text_effects == __o.text_effects
        )
