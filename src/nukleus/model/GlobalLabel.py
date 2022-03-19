from __future__ import annotations

from typing import List, cast

from .SchemaElement import POS_T
from .PositionalElement import PositionalElement, ffmt
from .Property import Property
from .TextEffects import TextEffects
from ..SexpParser import SEXP_T

class GlobalLabel(PositionalElement):
    """
    The global_label token defines a label name that is visible across all
    schematics in a design. This section will not exist if no global labels
    are defined in the schematic.
    """
    def __init__(self, **kwargs) -> None:
        self.text = kwargs.get("text", "")
        """The TEXT is a quoted string that defines the global label."""
        self.shape = kwargs.get("shape", "")
        """The shape token attribute defines the way the global label
        is drawn. See table below for global label shapes."""
        self.autoplaced = kwargs.get("autoplaced", "")
        """The optional fields_autoplaced is a flag that indicates
        that any PROPERTIES associated with the global label
        have been place automatically."""
        self.text_effects = kwargs.get("text_effects", TextEffects())
        """The TEXT_EFFECTS section defines how the global label text is drawn."""
        self.properties = kwargs.get("properties", [])
        """The PROPERTIES section defines the properties of the global label.
        Currently, the only supported property is the inter-sheet reference."""
        super().__init__(
            kwargs.get("identifier", None),
            kwargs.get("pos", ((0, 0), (0, 0))),
            kwargs.get("angle", 0),
        )

    @classmethod
    def parse(cls, sexp: SEXP_T) -> GlobalLabel:
        """Parse the sexp input.

        :param sexp SEXP_T: Sexp as List.
        :rtype GlobalLabel: The GlobalLabel Object.
        """
        _identifier = None
        _pos: POS_T = (0, 0)
        _angle: float = 0
        _text: str = cast(str, sexp[1])
        _shape: str = ""
        _autoplaced: str = ""
        _text_effects: TextEffects = TextEffects()
        _properties: List[Property] = []

        for token in sexp[2:]:
            if token[0] == 'at':
                _pos = (float(token[1]), float(token[2]))
                if len(token) == 4:
                    _angle = float(token[3])
            elif token[0] == 'uuid':
                _identifier = token[1]
            elif token[0] == 'effects':
                _text_effects = TextEffects.parse(cast(SEXP_T, token))
            elif token[0] == 'shape':
                _shape = token[1]
            elif token[0] == 'fields_autoplaced':
                _autoplaced = token[0]
            elif token[0] == 'property':
                _properties.append(Property.parse(cast(SEXP_T, token)))
            else:
                raise ValueError(f"unknown GlobalLabel element {token}")

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
            f"(at {ffmt(self.pos[0])} {ffmt(self.pos[1])} {ffmt(self.angle)})"
            f'{"" if self.autoplaced == "" else " (fields_autoplaced)"}'
        )
        strings.append(self.text_effects.sexp(indent=indent + 1))
        strings.append(f'{"  " * (indent + 1)}(uuid {self.identifier})')
        for prop in self.properties:
            strings.append(prop.sexp(indent=indent + 1))
        strings.append(f'{"  " * indent})')
        return "\n".join(strings)
