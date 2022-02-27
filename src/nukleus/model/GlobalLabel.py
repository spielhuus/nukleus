from __future__ import annotations

from typing import List, cast

from .PositionalElement import PositionalElement, POS_T
from .Property import Property
from .TextEffects import TextEffects
from ..SexpParser import SEXP_T

class GlobalLabel(PositionalElement):
    """
    The global_label token defines a label name that is visible across all
    schematics in a design. This section will not exist if no global labels
    are defined in the schematic.
    """

    text: str
    shape: str
    autoplaced: str
    text_effects: TextEffects
    properties: List[Property]

    def __init__(self, **kwargs) -> None:
        self.text = kwargs.get("text", "")
        self.shape = kwargs.get("shape", "")
        self.autoplaced = kwargs.get("autoplaced", "")
        self.text_effects = kwargs.get("text_effects", ("", TextEffects()))
        self.properties = kwargs.get("properties", ("", []))
        super().__init__(
            kwargs.get("identifier", None),
            kwargs.get("pos", ((0, 0), (0, 0))),
            kwargs.get("angle", 0),
        )

    @classmethod
    def parse(cls, sexp: SEXP_T) -> GlobalLabel:
        _identifier = None
        _pos: POS_T = (0, 0)
        _angle: float = 0
        _text: str = cast(str, sexp[1])
        _shape: str = ""
        _autoplaced: str = ""
        _text_effects: TextEffects = TextEffects()
        _properties: List[Property] = []

        for token in sexp[2:]:
            match token:
                case ["at", x, y, angle]:
                    _pos = (float(x), float(y))
                    _angle = float(angle)
                case ["at", x, y]:
                    _pos = (float(x), float(y))
                case ["uuid", identifier]:
                    _identifier = identifier
                case ["effects", *_]:
                    _text_effects = TextEffects.parse(cast(SEXP_T, token))
                case ["shape", shape]:
                    _shape = shape
                case ["fields_autoplaced"]:
                    _autoplaced = "fields_autoplaced"
                case ["property", *_]:
                    _properties.append(Property.parse(cast(SEXP_T, token)))
                case _:
                    raise ValueError(f"unknown label element {token}")

        return GlobalLabel(
            identifier=_identifier,
            pos=_pos,
            angle=_angle,
            text=_text,
            shape=_shape,
            autoplaced=_autoplaced,
            text_effects=_text_effects,
            properties=_properties,
        )

    def sexp(self, indent: int = 1) -> str:
        """
        Output the element as sexp string.

        :param indent [int]: indent count for this element.
        :rtype str: sexp string.
        """
        strings: List[str] = []
        strings.append(
            f'{"  " * indent}(global_label "{self.text}" (shape {self.shape}) '
            f"(at {self.pos[0]:g} {self.pos[1]:g} {self.angle:g})"
            f'{"" if self.autoplaced == "" else " (fields_autoplaced)"}'
        )
        strings.append(self.text_effects.sexp(indent=indent + 1))
        strings.append(f'{"  " * (indent + 1)}(uuid {self.identifier})')
        for prop in self.properties:
            strings.append(prop.sexp(indent=indent + 1))
        strings.append(f'{"  " * indent})')
        return "\n".join(strings)
