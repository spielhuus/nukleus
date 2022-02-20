from __future__ import annotations

from typing import Any, List

from ..SexpParser import SEXP_T
from .SchemaElement import POS_T
from .TextEffects import TextEffects
from .Utils import ffmt


class Property:
    """
    The property token defines a key value pair for storing user defined information.
    """

    key: str
    value: str
    id: str
    pos: POS_T
    angle: float
    text_effects: TextEffects | None

    def __init__(self, **kwargs) -> None:
        self.key = kwargs.get("key", "")
        self.value = kwargs.get("value", "")
        self.pos = kwargs.get("pos", (0, 0))
        self.angle = kwargs.get("angle", 0)
        self.id = kwargs.get("id", 0)
        self.text_effects = kwargs.get("text_effects", TextEffects())

    @classmethod
    def parse(cls, sexp: SEXP_T) -> Property:
        _key: str = sexp[1]
        _value: str = sexp[2]
        _id: int = 0
        _pos: POS_T = (0, 0)
        _angle: float = 0
        _text_effects: TextEffects|None = None

        for token in sexp[3:]:
            match token:
                case ["at", x, y, angle]:
                    _pos = (float(x), float(y))
                    _angle = float(angle)
                case ["at", x, y]:
                    _pos = (float(x), float(y))
                case ["id", id]:
                    _id = int(id)
                case ["effects", *_]:
                    _text_effects = TextEffects.parse(token)
                case _:
                    raise ValueError(f"unknown property element {token}")

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
